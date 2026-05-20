#include <iostream>
#include <cstdlib> // For std::atoi
#include "TH1F.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TCanvas.h"



/// This program inputs three raw mass spectra parameters (first M/Z, step, amount of steps); raw mass spectra itself and PPMs of gases in known mixture
/// Outputs coefficients of every gas 



int main(int argc, char* argv[]) {

    //start of input block


    // Check quantity of arguements provided
    //if (argc != 56) {
    //    std::cerr << "String of 56 float required" << std::endl;
    //    return 1; // Return error code 1 for incorrect usage
    //}

    

        // first three input entries - parameters of mass spectra:

    double initial_MZ = std::atoi(argv[0]);
    int MZ_step = std::atoi(argv[1]);
    int amount_of_steps = std::atoi(argv[2]);

    double unprocessed_mass_spectra[amount_of_steps];


    // Entries from 3 until 3+amount_of_steps are unprocessed mass spectra

    for(int i=0; i < amount_of_steps; i++){
        unprocessed_mass_spectra[i] = std::atoi(argv[3+i]);


    };

        // last six double floats are coefficients for computing (subject to change later)

    double helium_PPM = std::atoi(argv[4+amount_of_steps]);
    double argon_PPM = std::atoi(argv[5+amount_of_steps]);
    double oxygen_PPM = std::atoi(argv[6+amount_of_steps]);
    double nitrogen_PPM = std::atoi(argv[7+amount_of_steps]);
    double co2_PPM = std::atoi(argv[8+amount_of_steps]);
    double ch4_PPM = std::atoi(argv[9+amount_of_steps]);

    // end of input block




            // calculation code will be there later




    // start of output block

    double helium_coefficient = 0;
    double argon_coefficient = 0;
    double oxygen_coefficient = 0;
    double nitrogen_coefficient = 0;
    double co2_coefficient = 0;
    double ch4_coefficient = 0;
    
    std::cout << helium_coefficient << "," << argon_coefficient << "," << oxygen_coefficient << "," << nitrogen_coefficient << "," << co2_coefficient << "," << ch4_coefficient << "," << std::endl;


    // end of output block

    return 0; // Successful execution
}

/// to compile type:
///   g++ root_test.C $(root-config --glibs --cflags --libs) -o compiledtest


/// to execute via Python3:
///   CSV_concentrations = subprocess.run(["input_test",comma-separated-arguements],capture_output=True,cwd=cwd)
///   #cwd parsed by Python from Config file. All arguements (script name and ints/floats) are provided as list

