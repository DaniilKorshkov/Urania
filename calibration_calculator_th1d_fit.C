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




/// This program inputs five raw mass spectra parameters (first M/Z, step, amount of steps, amount of coefficients, amount of RGA scans, amount of parameters); dump of raw RGA scans and indexation of calibration coefficients (# of compound from 0 to 5, and M/Z)
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
        int mz_closest_integer = mz_remainder;
        
        
        // All calibration parameters are checked if they fit
        for(int i=0;i<amount_of_calibration_parameters;i++){

            
            
            // If M/Z for calibration parameter equals *M/Z as a variable, proceed further:
            if((mz_closest_integer == calibration_parameters_mz_index[i])&&((mz_remainder-mz_closest_integer)>0.45)&&((mz_remainder-mz_closest_integer)<0.55)){

           

            // Ionic current is appended by product of PPM of the specified compound multiplied by calibration factor
            ret += (calibration_parameter_array[i])*(ppm_array_matrix[calibration_parameters_per_element_index[i]][current_scan_number]) ;

            
            
        }}

        // Last (amount_of_rga_scans-1) parameters - daily variance in RGA sensitivity
        if(current_scan_number>0){ret = ret*calibration_parameter_array[amount_of_calibration_parameters+current_scan_number];}
        

        return ret; }; // This function returns Ionic Current with M/Z as variable, PPM's as variable parameters, calibration as static parameters






int main(int argc, char* argv[]) {


    //start of input block



    //Check if amount_of_steps argument is provided
    if (argc < 5 ) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; } 

    
    // first three input entries - parameters of mass spectra:
    double initial_MZ = std::atoi(argv[1]); int MZ_step = std::atoi(argv[2]); amount_of_steps = std::atoi(argv[3]); int amount_of_rga_scans = std::atoi(argv[4]); amount_of_calibration_parameters = std::atoi(argv[5]);

    std::cout << "amt  of scans" << amount_of_rga_scans << std::endl;
    std::cout << "amt  of params" << amount_of_calibration_parameters << std::endl;

    
    
    

    //Check quantity of arguements provided. This step is CRUCIAL to prevent program from accessing memory outside stack
    if (argc != (6 + amount_of_rga_scans*amount_of_steps + amount_of_rga_scans*6 + 2*amount_of_calibration_parameters) ) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; };
    

    //definition of PPM matrix

    for(int i=0;i < amount_of_rga_scans;i++ ){
        for(int j =0; j < 6; j++){
        ppm_array_matrix[j][i] = std::atoi(argv[6+amount_of_rga_scans*amount_of_steps + i*6 + j]);
        std::cout << "ppm" << " " << j << " " << i << " "<< std::atoi(argv[6+amount_of_rga_scans*amount_of_steps + i*6 + j]) << std::endl;
        }
        
    }



    
    
    
    // Indexation of calibration parameters
    for(int i=0;i < amount_of_calibration_parameters;i++ ){

        calibration_parameters_mz_index[i] = std::atoi(argv[7+amount_of_rga_scans*amount_of_steps + 6*amount_of_rga_scans +2*i]);
        calibration_parameters_per_element_index[i] = std::atoi(argv[6+amount_of_rga_scans*amount_of_steps + 6*amount_of_rga_scans +2*i]);

        std::cout << "mz index" << std::atoi(argv[7+amount_of_rga_scans*amount_of_steps + 6*amount_of_rga_scans +2*i]) << std::endl;
        std::cout << "element index" << std::atoi(argv[6+amount_of_rga_scans*amount_of_steps + 6*amount_of_rga_scans +2*i]) << std::endl;
        
    }
    
    std::cout << ppm_array_matrix[0][0] << std::endl;
    

    

    // Definition of histogram
    TH1D* rga_scan_histogram_pointer = new TH1D("h", "rga", (amount_of_steps*amount_of_rga_scans), (initial_MZ), (initial_MZ + (amount_of_rga_scans*amount_of_steps*MZ_step)));
    
        for(int i=0;i<(amount_of_steps*amount_of_rga_scans);i++){
            double current_mz = initial_MZ + MZ_step*i;
            double ionic_current = std::atoi(argv[6+i]);

            std::cout << "MZ: " << (initial_MZ + MZ_step*i) << ", bin: " << ionic_current << std::endl;

            //std::cout << "RGA scan" << current_mz << ": " << ionic_current << std::endl;
            rga_scan_histogram_pointer->SetBinContent( current_mz, ionic_current);
        }


    for(int i = 0; i < (amount_of_rga_scans*amount_of_steps); i++){

            std::cout << "RGA scan " << i << ": " << rga_scan_histogram_pointer->GetBinContent(i) << std::endl;
            

    }

    // end of input block





    // beginning of calculator block



    // Wrap fitting step-function function into TF1 class with initial guess for all parameters (ppm's)
    TF1 ffit("ffit",ionic_current_fit_for_specific_mz, initial_MZ , (initial_MZ + (amount_of_steps*MZ_step*amount_of_rga_scans)) ,(amount_of_calibration_parameters+amount_of_rga_scans-1));
    for(int i=0;i<(amount_of_calibration_parameters+amount_of_rga_scans-1);i++){

        // Last (amount_of_rga_scans-1) parameters - daily variance in RGA sensitivity
        if(i<amount_of_calibration_parameters){ffit.SetParameters(i,0.1);}else{ffit.SetParameters(i,1); ffit.SetParLimits(i, 0.7, 1.3);};}  

    
    // Fitting function iteslf
    TFitResultPtr calibration_fit_values = rga_scan_histogram_pointer->Fit(&ffit,"S");



    // end of calculator block





    // start of output block


    //Inquiry of obtained fit values from TFitResultPtr class
   


    for(int i = 0;i<amount_of_calibration_parameters;i++){
        std::cout << calibration_fit_values->Parameter(i) << " " << std::endl;






    }
    
    // end of output block

    TCanvas *c1 = new TCanvas("c1", "Random Histogram", 800, 600);
    rga_scan_histogram_pointer->Draw();
    c1->SaveAs("cal_histogram.png");




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