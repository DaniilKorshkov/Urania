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

    double initial_MZ = std::atoi(argv[1]);
    int MZ_step = std::atoi(argv[2]);
    int amount_of_steps = std::atoi(argv[3]);

    



    //Check quantity of arguements provided. This step is CRUCIAL to prevent program from accessing memory outside stack
    if (argc != (10 + amount_of_steps) ) {
        std::cerr << "Incorrect amount of args provided" << std::endl;
        return 1; // Return error code 1 for incorrect usage
    }



    /// std::cout << initial_MZ << MZ_step << amount_of_steps <<std::endl;

    double unprocessed_mass_spectra[amount_of_steps];


    // Entries from 3 until 3+amount_of_steps are unprocessed mass spectra

    for(int i=0; i < amount_of_steps; i++){
        unprocessed_mass_spectra[i] = std::atoi(argv[4+i]);
         std::cout << unprocessed_mass_spectra[i] << std::endl;

    };

        // last six double floats are coefficients for computing (subject to change later)

    double helium_4 = std::atoi(argv[4 + amount_of_steps]);
    double argon_40 = std::atoi(argv[5 + amount_of_steps]);
    double oxygen_32 = std::atoi(argv[6 + amount_of_steps]);
    double nitrogen_28 = std::atoi(argv[7 + amount_of_steps]);
    double co2_44 = std::atoi(argv[8 + amount_of_steps]);
    double ch4_15 = std::atoi(argv[9 + amount_of_steps]);

    std::cout << helium_4 << "," << ch4_15 << std::endl;


    double helium_mask[amount_of_steps]; std::fill_n(helium_mask, amount_of_steps, 0);
    double argon_mask[amount_of_steps]; std::fill_n(argon_mask, amount_of_steps, 0);
    double oxygen_mask[amount_of_steps]; std::fill_n(oxygen_mask, amount_of_steps, 0);
    double nitrogen_mask[amount_of_steps]; std::fill_n(nitrogen_mask, amount_of_steps, 0);
    double co2_mask[amount_of_steps]; std::fill_n(co2_mask, amount_of_steps, 0);
    double ch4_mask[amount_of_steps]; std::fill_n(ch4_mask, amount_of_steps, 0);

    bool non_zero_masks[6]; std::fill_n(non_zero_masks, 6, false);  // array to define what of the masks above are non-zero
    int non_zero_masks_quantity = 0;


    if( (initial_MZ <= 4) && ( (initial_MZ + MZ_step*amount_of_steps) >= 4 ) )
    {int step_count = initial_MZ/MZ_step;
    helium_mask[4 - step_count] = helium_4;
    non_zero_masks[0] = true; };

    if( (initial_MZ <= 40) && ( (initial_MZ + MZ_step*amount_of_steps) >= 40 ) )
    {int step_count = initial_MZ/MZ_step;
    argon_mask[40 - step_count] = argon_40;
    non_zero_masks[1] = true; };

    if( (initial_MZ <= 32) && ( (initial_MZ + MZ_step*amount_of_steps) >= 32 ) )
    {int step_count = initial_MZ/MZ_step;
    oxygen_mask[32 - step_count] = oxygen_32;
    non_zero_masks[2] = true; };

    if( (initial_MZ <= 28) && ( (initial_MZ + MZ_step*amount_of_steps) >= 28 ) )
    {int step_count = initial_MZ/MZ_step;
    nitrogen_mask[28 - step_count] = nitrogen_28;
    non_zero_masks[3] = true; };

    if( (initial_MZ <= 44) && ( (initial_MZ + MZ_step*amount_of_steps) >= 44 ) )
    {int step_count = initial_MZ/MZ_step;
    co2_mask[44 - step_count] = co2_44;
    non_zero_masks[4] = true; };

    if( (initial_MZ <= 15) && ( (initial_MZ + MZ_step*amount_of_steps) >= 15 ) )
    {int step_count = initial_MZ/MZ_step;
    ch4_mask[15 - step_count] = ch4_15;
    non_zero_masks[5] = true; };

    
    for(i = 0, i < 6, i++){
        if(non_zero_masks[i]){
            non_zero_masks_quantity ++;
        };
    };


    
    
    


    // end of input block









    // beginning of calculator block

    // refer to following link for documentation: https://root.cern.ch/root/htmldoc/guides/users-guide/LinearAlgebra.html
            
    // use TMatrixD ; TVectorD ; TDecompSVD


    // end of calculator block









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

