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




/// This program inputs three raw mass spectra parameters (first M/Z, step, amount of steps); raw mass spectra itself and coefficients as space-separated numbers
/// Outputs PPM of every gas in mixture as space separated numbers




// Definition of global variables begin

// caliration variables are declared as globals to easily pass to fitting function
double helium_4; double argon_40; double oxygen_32; double nitrogen_28; double co2_44; double ch4_15;

// Definition of global variables end




// step-function for emulating RGA raw output (m/z is a variable, PPM's are parameters) for fitting purpose
Double_t ionic_current_fit_for_specific_mz(double *mz, double *ppm_array){  
    
        Double_t ret; ret = 0;    
    
        if((*mz > 4)&&(*mz < 5)){ret = helium_4*ppm_array[0];};
        if((*mz > 15)&&(*mz < 16)){ret = ch4_15*ppm_array[1];}; 
        if((*mz > 28)&&(*mz < 29)){ret = nitrogen_28*ppm_array[2];};
        if((*mz > 32)&&(*mz < 33)){ret = oxygen_32*ppm_array[3];};
        if((*mz > 40)&&(*mz < 41)){ret = argon_40*ppm_array[4];};
        if((*mz > 44)&&(*mz < 45)){ret = co2_44*ppm_array[5];};
        
        return ret; }; // This function returns Ionic Current with M/Z as variable, PPM's as variable parameters, calibration as static parameters






int main(int argc, char* argv[]) {



    //start of input block



    //Check if amount_of_steps argument is provided
    if (argc < 3 ) { std::cerr << "Incorrect amount of args provided" << std::endl; return 1; } 

    
    // first three input entries - parameters of mass spectra:
    double initial_MZ = std::atoi(argv[1]); int MZ_step = std::atoi(argv[2]); int amount_of_steps = std::atoi(argv[3]);


    //Check quantity of arguements provided. This step is CRUCIAL to prevent program from accessing memory outside stack
    if (argc != (10 + amount_of_steps) ) { std::cerr << "Incorrect amount of args provided" << std::endl; return 1; }


    // Last six (subject to change later, simple model was used for the testing purpose) arguments - calibration parameters for every compound in the system
    helium_4 = std::atoi(argv[4 + amount_of_steps]); argon_40 = std::atoi(argv[5 + amount_of_steps]); oxygen_32 = std::atoi(argv[6 + amount_of_steps]); nitrogen_28 = std::atoi(argv[7 + amount_of_steps]); co2_44 = std::atoi(argv[8 + amount_of_steps]); ch4_15 = std::atoi(argv[9 + amount_of_steps]);


    // Definition of histogram
    TH1D* rga_scan_histogram_pointer = new TH1D("h", "rga", amount_of_steps, (initial_MZ-0.5), (0.5+initial_MZ + (amount_of_steps*MZ_step)));

        for(int i=0;i<amount_of_steps;i++){
            double current_mz = initial_MZ + MZ_step*i;
            double ionic_current = std::atoi(argv[4+i]);
            rga_scan_histogram_pointer->SetBinContent( current_mz, ionic_current);
        };



    // end of input block





    // beginning of calculator block



    // Wrap fitting step-function function into TF1 class with initial guess for all parameters (ppm's)
    TF1 ffit("ffit",ionic_current_fit_for_specific_mz, initial_MZ , (initial_MZ + (amount_of_steps*MZ_step)) ,6);  
    ffit.SetParameters(0, 0.5); ffit.SetParameters(1, 0.5); ffit.SetParameters(2, 0.5); ffit.SetParameters(3, 0.5); ffit.SetParameters(4, 0.5); ffit.SetParameters(5, 0.5);

    
    // Fitting function iteslf
    TFitResultPtr ppm_fit_values = rga_scan_histogram_pointer->Fit(&ffit,"S");



    // end of calculator block





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

