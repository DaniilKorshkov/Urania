#include <iostream>
#include <cstdlib> // For std::atoi
#include <stack>
#include "TH1D.h"
#include "TF1.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TCanvas.h"
#include "TMatrixD.h"
#include "TDecompSVD.h"
#include "TFitResult.h"
#include "TFitResultPtr.h"
#include "Math/Functor.h"
#include <Math/SMatrix.h>




/// This program inputs three raw mass spectra parameters (first M/Z, step, amount of steps, amount of coefficients); raw mass spectra itself and coefficients as space-separated numbers
/// Every coefficient is provided as three space-separated numbers: compound(0 from 6), M/Z, IC for pure compound
/// Compounds listed as following: He, Ar, O2, N2, CO2, CH4
/// Outputs PPM of every gas in mixture as space separated numbers




// Definition of global variables begin

// caliration variables are declared as globals to easily pass to fitting function

double ppm_array_matrix[6][255];
int amount_of_steps;
int amount_of_calibration_parameters;


int calibration_parameters_mz_index[255];
int calibration_parameters_per_element_index[255];


// Definition of global variables end




// step-function for emulating RGA raw output (m/z is a variable, PPM's are parameters) for fitting purpose
Double_t ionic_current_fit_for_specific_mz(double *mz, double *calibration_parameter_array){  
    
        Double_t ret; ret = 0;
        double mz_remainder = remainder(*mz,amount_of_steps);if(mz_remainder<0){mz_remainder+=amount_of_steps;};
        int current_scan_number = (*mz)/amount_of_steps;
        int mz_closest_integer = round(mz_remainder);
        
        
        for(int i=0;i<amount_of_calibration_parameters;i++){
            if(mz_closest_integer == calibration_parameters_mz_index[i]){
            ret += (calibration_parameter_array[i])*(ppm_array_matrix[calibration_parameters_per_element_index[i]][calibration_parameters_mz_index[i]]) ;
        }}

        return ret; }; // This function returns Ionic Current with M/Z as variable, PPM's as variable parameters, calibration as static parameters






int main(int argc, char* argv[]) {


    //start of input block



    //Check if amount_of_steps argument is provided
    if (argc < 5 ) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; } 

    
    // first three input entries - parameters of mass spectra:
    double initial_MZ = std::atoi(argv[1]); int MZ_step = std::atoi(argv[2]); amount_of_steps = std::atoi(argv[3]); int amount_of_rga_scans = std::atoi(argv[4]); amount_of_calibration_parameters = std::atoi(argv[5]);


    

    //Check quantity of arguements provided. This step is CRUCIAL to prevent program from accessing memory outside stack
    if (argc != (5 + amount_of_rga_scans*amount_of_steps + amount_of_rga_scans*6 + 2*amount_of_calibration_parameters) ) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; };
    


    // Definition of calibration parameter matrix
    
    

    for(int i=0;i < amount_of_calibration_parameters;i++ ){

        calibration_parameters_mz_index[i] = std::atoi(argv[6+amount_of_rga_scans*amount_of_steps + 6*amount_of_rga_scans +2*i]);
        calibration_parameters_per_element_index[i] = std::atoi(argv[5+amount_of_rga_scans*amount_of_steps+ 6*amount_of_rga_scans +2*i]);
        
    }
    
    

    // Definition of histogram
    TH1D* rga_scan_histogram_pointer = new TH1D("h", "rga", amount_of_steps, (initial_MZ-0.5), (0.5+initial_MZ + (amount_of_rga_scans*amount_of_steps*MZ_step)));

        for(int i=0;i<(amount_of_steps*amount_of_rga_scans);i++){
            double current_mz = initial_MZ + MZ_step*i;
            double ionic_current = std::atoi(argv[6+i]);
            rga_scan_histogram_pointer->SetBinContent( current_mz, ionic_current);
        }


        for(int i; i<amount_of_calibration_parameters; i++){

            calibration_parameters_mz_index[i] = std::atoi(argv[7+ amount_of_steps*amount_of_rga_scans + i]);
            calibration_parameters_per_element_index[i] = std::atoi(argv[6+ amount_of_steps*amount_of_rga_scans + i]);




        }














    // end of input block





    // beginning of calculator block



    // Wrap fitting step-function function into TF1 class with initial guess for all parameters (ppm's)
    TF1 ffit("ffit",ionic_current_fit_for_specific_mz, initial_MZ , (initial_MZ + (amount_of_steps*MZ_step*amount_of_rga_scans)) ,amount_of_calibration_parameters);
    for(int i=0;i<amount_of_calibration_parameters;i++){ffit.SetParameters(i,0.5);}  

    
    // Fitting function iteslf
    TFitResultPtr calibration_fit_values = rga_scan_histogram_pointer->Fit(&ffit,"S");



    // end of calculator block





    // start of output block


    //Inquiry of obtained fit values from TFitResultPtr class
   


    for(int i = 0;i<amount_of_calibration_parameters;i++){
        std::cout << calibration_fit_values->Parameter(i) << " " << std::endl;






    }
    
    // end of output block




    return 0; // Successful execution
}



/// to compile type:
///   g++ calibration_calculator_th1d_fit.C $(root-config --glibs --cflags --libs) -o calibration_calculator


/// to execute via Python3:
///   CSV_concentrations = subprocess.run(["input_test",comma-separated-arguements],capture_output=True,cwd=cwd)
///   #cwd parsed by Python from Config file. All arguements (script name and ints/floats) are provided as list



/// How to pass args:
/// First 5 entries - initial_MZ, MZ_step, amount_of_steps, amount_of_rga_scans, amount_of_calibration_parameters
/// Then - space-separated dump rga_scans
/// Then - space-separated element_index and mz_index of every calibration parameter