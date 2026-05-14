#include <iostream>
#include <cstdlib> // For std::atoi
#include "TH1F.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TCanvas.h"



/// This program inputs three raw mass spectra parameters (first M/Z, step, amount of steps); raw mass spectra itself and coefficients as space-separated numbers
/// Outputs PPM of every gas in mixture 



int main(int argc, char* argv[]) {

    //start of input block



    //Check if amount_of_steps argument is provided
    if (argc < 3 ) {
        std::cerr << "Incorrect amount of args provided" << std::endl;
        return 1; // Return error code 1 for incorrect usage
    } 

    

    

        // first three input entries - parameters of mass spectra:

    double initial_MZ = std::atoi(argv[0]);
    int MZ_step = std::atoi(argv[1]);
    int amount_of_steps = std::atoi(argv[2]);



    //Check quantity of arguements provided. This step is CRUCIAL to prevent program from accessing memory outside stack
    if (argc != (11 + amount_of_steps) ) {
        std::cerr << "Incorrect amount of args provided" << std::endl;
        return 1; // Return error code 1 for incorrect usage
    }



    /// std::cout << initial_MZ << MZ_step << amount_of_steps <<std::endl;

    double unprocessed_mass_spectra[amount_of_steps];


    // Entries from 3 until 3+amount_of_steps are unprocessed mass spectra

    for(int i=0; i < amount_of_steps; i++){
        unprocessed_mass_spectra[i] = std::atoi(argv[3+i]);


    };

        // last six double floats are coefficients for computing (subject to change later)

    double helium_coefficient = std::atoi(argv[5 + amount_of_steps]);
    double argon_coefficient = std::atoi(argv[6 + amount_of_steps]);
    double oxygen_coefficient = std::atoi(argv[7 + amount_of_steps]);
    double nitrogen_coefficient = std::atoi(argv[8 + amount_of_steps]);
    double co2_coefficient = std::atoi(argv[9 + amount_of_steps]);
    double ch4_coefficient = std::atoi(argv[10 + amount_of_steps]);


    std::cout << helium_coefficient << ";" << ch4_coefficient << std::endl;
    




    // end of input block




            // calculation code will be there later




    // start of output block

    double helium_ppm = 0;
    double argon_ppm = 0;
    double oxygen_ppm = 0;
    double nitrogen_ppm = 0;
    double co2_ppm = 0;
    double ch4_ppm = 0;
    
    std::cout << helium_ppm << "," << argon_ppm << "," << oxygen_ppm << "," << nitrogen_ppm << "," << co2_ppm << "," << ch4_ppm << std::endl;


    // end of output block

    return 0; // Successful execution
}

/// to compile type:
///   g++ root_test.C $(root-config --glibs --cflags --libs) -o compiledtest


/// to execute via Python3:
///   CSV_concentrations = subprocess.run(["input_test",comma-separated-arguements],capture_output=True,cwd=cwd)
///   #cwd parsed by Python from Config file. All arguements (script name and ints/floats) are provided as list

