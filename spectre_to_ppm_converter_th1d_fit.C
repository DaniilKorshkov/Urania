#include <iostream>
#include <cstdlib> // For std::atoi
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

double calibration_matrix[6][255];


// Definition of global variables end




// step-function for emulating RGA raw output (m/z is a variable, PPM's are parameters) for fitting purpose
Double_t ionic_current_fit_for_specific_mz(double *mz, double *ppm_array){  
    
        Double_t ret; ret = 0;
        int mz_closest_integer = *mz;
        
        
        for(int i=0;i<6;i++){
            if(((*mz-mz_closest_integer)>0.45)&&((*mz-mz_closest_integer)<0.55)){
                ret += (calibration_matrix[i][mz_closest_integer])*(ppm_array[i]);}
        };

        return ret; }; // This function returns Ionic Current with M/Z as variable, PPM's as variable parameters, calibration as static parameters






int main(int argc, char* argv[]) {


    //start of input block



    //Check if amount_of_steps argument is provided
    if (argc < 4 ) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; } 

    
    // first three input entries - parameters of mass spectra:
    double initial_MZ = std::atof(argv[1]); double MZ_step = std::atof(argv[2]); int amount_of_steps = std::atoi(argv[3]); int amount_of_calibration_parameters = std::atoi(argv[4]);


    

    //Check quantity of arguements provided. This step is CRUCIAL to prevent program from accessing memory outside stack
    if (argc != (5 + amount_of_steps + 3*amount_of_calibration_parameters) ) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; };
    


    // Definition of calibration parameter matrix
    for(int i=0;i<255;i++){for(int j=0;j<6;j++){calibration_matrix[j][i] = 0.0;}}
    

    for(int i=0;i < amount_of_calibration_parameters;i++ ){

        
        calibration_matrix[std::atoi(argv[5+amount_of_steps+(3*i)])][std::atoi(argv[6+amount_of_steps+(3*i)])] = std::atof(argv[7+amount_of_steps+(3*i)]);
        //std::cout << std::atoi(argv[5+amount_of_steps+(3*i)]) << " "<< std::atoi(argv[6+amount_of_steps+(3*i)]) << " " << std::atoi(argv[7+amount_of_steps+(3*i)]) << std::endl;

    }
    
    

    // Definition of histogram
    TH1D* rga_scan_histogram_pointer = new TH1D("h", "rga", amount_of_steps, 1, (1 + (amount_of_steps*MZ_step)));

        for(int i=0;i<amount_of_steps;i++){
            double current_mz = initial_MZ + MZ_step*i;
            double ionic_current = std::atof(argv[5+i]);
            rga_scan_histogram_pointer->SetBinContent( current_mz, ionic_current);
        }

















    // end of input block





    // beginning of calculator block



    // Wrap fitting step-function function into TF1 class with initial guess for all parameters (ppm's)
    TF1 ffit("ffit",ionic_current_fit_for_specific_mz, initial_MZ , (initial_MZ + (amount_of_steps*MZ_step)) ,6);  
    ffit.SetParameters(0, 0.5); ffit.SetParameters(1, 0.5); ffit.SetParameters(2, 0.5); ffit.SetParameters(3, 0.5); ffit.SetParameters(4, 0.5); ffit.SetParameters(5, 0.5);

    
    // Fitting function iteslf
    TFitResultPtr ppm_fit_values = rga_scan_histogram_pointer->Fit(&ffit,"S");



    // end of calculator block



    TCanvas *c1 = new TCanvas("c1", "Random Histogram", 800, 600);
    rga_scan_histogram_pointer->Draw();
    c1->SaveAs("scan_histogram.png");



    // start of output block


    //Inquiry of obtained fit values from TFitResultPtr class
    double he_ppm = ppm_fit_values->Parameter(0); double ar_ppm = ppm_fit_values->Parameter(1); double o2_ppm = ppm_fit_values->Parameter(2); double n2_ppm = ppm_fit_values->Parameter(3); double co2_ppm = ppm_fit_values->Parameter(4); double ch4_ppm = ppm_fit_values->Parameter(5);
    std::cout << he_ppm << " " << ar_ppm << " " << o2_ppm << " " << n2_ppm << " " << co2_ppm << " " << ch4_ppm << std::endl;

    // end of output block




    return 0; // Successful execution
}



/// to compile type:
///   g++ spectre_to_ppm_converter_th1d_fit.C $(root-config --glibs --cflags --libs) -o spectre_to_ppm_converter


/// to execute via Python3:
///   CSV_concentrations = subprocess.run(["input_test",comma-separated-arguements],capture_output=True,cwd=cwd)
///   #cwd parsed by Python from Config file. All arguements (script name and ints/floats) are provided as list

