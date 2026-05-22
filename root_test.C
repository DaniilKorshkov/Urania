#include <iostream>
#include <cstdlib> // For std::atoi



int main(int argc, char* argv[]) {
    // Check if two arguments are provided
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <integer1> <integer2>" << std::endl;
        return 1; // Return error code 1 for incorrect usage
    }

    // Convert the arguments from strings to integers
    float num1 = std::atof(argv[1]);
    float num2 = std::atof(argv[2]);

    // Calculate and print the sum
    float sum = num1 + num2;
    float product = num1*num2;
    std::cout << sum << " " << product << std::endl;






    // Create a 1D histogram: name, title, bins, x_min, x_max
            ///TH1F *hist = new TH1F("hist", "Basic Histogram;X axis;Counts", 100, -5, 5);

    // Fill with random Gaussian data
    ///TRandom3 rng(42);
    ///for (int i = 0; i < 10000; i++) {
    ///    hist->Fill(rng.Gaus(0, 1));
    ///}







        // Save to a ROOT file
    ///TFile *file = new TFile("histogram.root", "RECREATE");
    ///hist->Write();
    ///file->Close();

    ///delete hist;
    ///delete file;





    










    return 0; // Successful execution
}

/// to compile type:
///   g++ root_test.C $(root-config --glibs --cflags --libs) -o compiledtest