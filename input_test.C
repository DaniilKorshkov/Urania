#include <iostream>
#include <cstdlib> // For std::atoi
#include "TH1F.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TCanvas.h"


int main(int argc, char* argv[]) {

    //start of input block


    // Check quantity of arguements provided
    if (argc != 56) {
        std::cerr << "String of 56 float required" << std::endl;
        return 1; // Return error code 1 for incorrect usage
    }

    

        // first 50 double floats are unprocessed mass spectra

    double unprocessed_mass_spectra[50];
    for(i=0, i<50, i++){
        unprocessed_mass_spectra[i] = std::atoi(argv[i])


    };

        // next six double floats are coefficients for computing (subject to change later)

    double helium_coefficient = std::atoi(argv[50]);
    double argon_coefficient = std::atoi(argv[51]);
    double oxygen_coefficient = std::atoi(argv[52]);
    double nitrogen_coefficient = std::atoi(argv[53]);
    double co2_coefficient = std::atoi(argv[54]);
    double ch4_coefficient = std::atoi(argv[55]);

    // end of input block




            // calculation code will be there later




    // start of output block

    double helium_ppm = 0;
    double argon_ppm = 0;
    double oxygen_ppm = 0;
    double nitrogen_ppm = 0;
    double co2_ppm = 0;
    double ch4_ppm = 0;
    
    std::cout << helium_ppm << "," << argon_ppm << "," << oxygen_ppm << "," << nitrogen_ppm << "," << co2_ppm << "," << ch4_ppm << "," << std::endl;


    // end of output block

    return 0; // Successful execution
}

/// to compile type:
///   g++ root_test.C $(root-config --glibs --cflags --libs) -o compiledtest


/// to execute via Python3:
///   CSV_concentrations = subprocess.run(["input_test",comma-separated-arguements],capture_output=True,cwd=cwd)
///   #cwd parsed by Python from Config file. All arguements (script name and 56 floats) are provided as list