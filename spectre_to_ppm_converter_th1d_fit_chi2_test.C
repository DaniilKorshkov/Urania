#include <iostream>
#include <cstdio>  // For std::sprintf
#include <cstdlib> // For std::atoi
#include "TH1D.h"
#include "TF1.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TMatrixD.h"
#include "TDecompSVD.h"
#include "TFitResult.h"
#include "TFitResultPtr.h"
#include "Math/Functor.h"
#include <Math/SMatrix.h>
#include <ctime>
#include "TPaveText.h"
#include "TGraph.h"




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
            if(((*mz-mz_closest_integer)>0)&&((*mz-mz_closest_integer)<1)){
                ret += (calibration_matrix[i][mz_closest_integer])*(ppm_array[i]);}
        };

        return ret; }; // This function returns Ionic Current with M/Z as variable, PPM's as variable parameters, calibration as static parameters






int main(int argc, char* argv[]) {


    //start of input block



    //Check if amount_of_steps argument is provided
    if (argc < 4 ) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; } 

    
    // first three input entries - parameters of mass spectra:
    double initial_MZ = std::atof(argv[1]); double MZ_step = std::atof(argv[2]); int amount_of_steps = std::atoi(argv[3]); int amount_of_calibration_parameters = std::atoi(argv[4]);


    

    // Optional trailing "-g" flag enables producing/saving graphs.
    int save_graphs = 0;
    if (argc > 1 && argv[argc - 1][0] == '-' && argv[argc - 1][1] == 'g' && argv[argc - 1][2] == '\0') {
        save_graphs = 1;
    }

    int expected_argc = 5 + amount_of_steps + 3 * amount_of_calibration_parameters;
    if (save_graphs) { expected_argc += 1; }

    //Check quantity of arguements provided. This step is CRUCIAL to prevent program from accessing memory outside stack
    if (argc != expected_argc) { std::cout << "Incorrect amount of args provided" << std::endl; return 1; };
    


    // Definition of calibration parameter matrix
    for(int i=0;i<255;i++){for(int j=0;j<6;j++){calibration_matrix[j][i] = 0.0;}}
    

    for(int i=0;i < amount_of_calibration_parameters;i++ ){

        
        calibration_matrix[std::atoi(argv[5+amount_of_steps+(3*i)])][std::atoi(argv[6+amount_of_steps+(3*i)])] = std::atof(argv[7+amount_of_steps+(3*i)]);
        //std::cout << std::atoi(argv[5+amount_of_steps+(3*i)]) << " "<< std::atoi(argv[6+amount_of_steps+(3*i)]) << " " << std::atoi(argv[7+amount_of_steps+(3*i)]) << std::endl;

    }
    
    

    // Definition of histogram
    TH1D* rga_scan_histogram_pointer = new TH1D("h", "RGA scan", amount_of_steps, 1, (1 + (amount_of_steps*MZ_step)));

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
    TFitResultPtr ppm_fit_values = rga_scan_histogram_pointer->Fit(&ffit,"S0");

    // Keep the fitted parameter values for the subsequent chi^2 scans.
    double fitted_params[6];
    for (int i = 0; i < 6; i++) { fitted_params[i] = ppm_fit_values->Parameter(i); }

    // Normalized parameters (absolute sum = 1000000) used for reporting.
    double normalized_params[6];
    double normalized_errors[6];
    double normalized_sum = 0.0;
    for (int i = 0; i < 6; i++) { normalized_sum += std::fabs(fitted_params[i]); }
    if (normalized_sum == 0.0) { normalized_sum = 1.0; }
    for (int i = 0; i < 6; i++) { normalized_params[i] = 1000000.0 * std::fabs(fitted_params[i]) / normalized_sum; }
    // Scale the raw fit uncertainties by the same normalization factor.
    for (int i = 0; i < 6; i++) { normalized_errors[i] = 1000000.0 * ppm_fit_values->ParError(i) / normalized_sum; }

    // Timestamp reused for the saved chi^2 plots.
    // A single timestamp used for every output file created by this run.
    std::time_t run_now = std::time(nullptr);
    std::tm* run_local_time = std::localtime(&run_now);
    char run_timestamp[64];
    std::strftime(run_timestamp, sizeof(run_timestamp), "%H:%M:%S-%d-%m-%Y", run_local_time);

    const char* chi2_param_names[6] = {"helium", "argon", "oxygen", "nitrogen", "CO2", "methane"};

    // After the fit is complete, vary each parameter individually while all
    // the other parameters stay fixed at their fitted values and record the
    // resulting chi^2. Produce and save a chi^2 vs. parameter plot for each.
    TGraph* chi2_graphs[6];
    TCanvas* chi2_combined_canvas = new TCanvas("chi2_combined", "Chi2 vs parameter", 1200, 800);
    chi2_combined_canvas->Divide(3, 2);

    for (int ipar = 0; ipar < 6; ipar++) {
        double err = ppm_fit_values->ParError(ipar);
        if (!(err > 1e-8)) { err = std::fabs(fitted_params[ipar]) * 0.1 + 0.1; }

        TGraph* g = new TGraph();
        char graph_title[128];
        std::sprintf(graph_title, "Chi2 vs %s (other parameters fixed)", chi2_param_names[ipar]);
        g->SetTitle(graph_title);
        g->SetMarkerStyle(20);
        g->SetMarkerSize(0.6);
        g->SetLineColor(kBlue);
        g->SetMarkerColor(kBlue);

        const int n_points = 201;
        double lo = fitted_params[ipar] - 5.0 * err;
        double hi = fitted_params[ipar] + 5.0 * err;
        if (lo == hi) { lo -= 0.5; hi += 0.5; }

        for (int k = 0; k <= n_points; k++) {
            double trial = lo + (hi - lo) * (double)k / (double)n_points;

            double params[6];
            for (int j = 0; j < 6; j++) { params[j] = fitted_params[j]; }
            params[ipar] = trial;

            double chi2 = 0.0;
            for (int bin = 1; bin <= rga_scan_histogram_pointer->GetNbinsX(); bin++) {
                double observed = rga_scan_histogram_pointer->GetBinContent(bin);
                double x_center = rga_scan_histogram_pointer->GetBinCenter(bin);
                double model_value = ionic_current_fit_for_specific_mz(&x_center, params);

                double bin_error = std::sqrt(std::fabs(observed));
                if (bin_error == 0.0) { bin_error = 1.0; }

                double residual = observed - model_value;
                chi2 += (residual * residual) / (bin_error * bin_error);
            }

            // Display the scanned parameter in normalized units.
            double normalized_trial = 1000000.0 * trial / normalized_sum;
            g->SetPoint(g->GetN(), normalized_trial, chi2);
        }

        g->GetXaxis()->SetTitle("Normalized parameter");
        g->GetYaxis()->SetTitle("Chi2");
        chi2_graphs[ipar] = g;

        // Draw on the combined (single) canvas.
        chi2_combined_canvas->cd(ipar + 1);
        g->Draw("APL");
    }

    if (save_graphs) {
        chi2_combined_canvas->cd();
        char combined_filename[256];
        std::sprintf(combined_filename, "chi2_vs_parameters_%s.png", run_timestamp);
        chi2_combined_canvas->SaveAs(combined_filename);
    }





    // end of calculator block



    TCanvas *c1 = new TCanvas("c1", "Random Histogram", 900, 600);
    c1->SetRightMargin(0.28);
    c1->SetLogy(1);
    rga_scan_histogram_pointer->SetStats(0);
    rga_scan_histogram_pointer->Draw("hist");

    const char* entry_names[6] = {"helium", "argon", "oxygen", "nitrogen", "CO2", "methane"};

    TLegend *legend = new TLegend(0.74, 0.5, 0.98, 0.88);

    TF1* comps[6];

    // Plot ionic_current_fit_for_specific_mz contribution with a different
    // colour for each entry of ppm_array (one curve per gas/compound).
    for (int i = 0; i < 6; i++) {
        double params[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
        params[i] = ppm_fit_values->Parameter(i);
        char name[64];
        std::sprintf(name, "comp_%d", i);
        TF1 *comp = new TF1(name, ionic_current_fit_for_specific_mz,
            initial_MZ, (initial_MZ + (amount_of_steps * MZ_step)), 6);
        for (int j = 0; j < 6; j++) { comp->SetParameter(j, params[j]); }
        comp->SetLineColor(i + 2);   // distinct colour per ppm_array entry
        comp->SetLineWidth(2);
        comp->Draw("same");

        comps[i] = comp;
    }

    int legend_order[6] = {0, 1, 2, 3, 5, 4};
    for (int k = 0; k < 6; k++) {
        int i = legend_order[k];
        legend->AddEntry(comps[i], entry_names[i], "l");
    }

    char chi2_text[128];
    std::sprintf(chi2_text, "Chi2 = %.6g", ppm_fit_values->Chi2());
    legend->AddEntry((TObject*)0, chi2_text, "");

    legend->SetFillStyle(0);
    legend->Draw();

    // Display the raw fit method output in a box below the histogram legend.
    TPaveText *fit_output_box = new TPaveText(0.74, 0.06, 0.98, 0.49, "NDC");
    fit_output_box->SetFillColor(kWhite);
    fit_output_box->SetBorderSize(1);
    fit_output_box->SetTextAlign(12);
    fit_output_box->SetTextSize(0.02);
    fit_output_box->SetMargin(0.01);
    char fit_output_line[256];
    std::sprintf(fit_output_line, "Normalized output (sum = 1e6):");
    fit_output_box->AddText(fit_output_line);
    for (int i = 0; i < 6; i++) {
        std::sprintf(fit_output_line, "p%d = %.6g +/- %.6g", i, normalized_params[i], normalized_errors[i]);
        fit_output_box->AddText(fit_output_line);
    }
    std::sprintf(fit_output_line, "Chi2 = %.6g", ppm_fit_values->Chi2());
    fit_output_box->AddText(fit_output_line);
    std::sprintf(fit_output_line, "NDf = %u", ppm_fit_values->Ndf());
    fit_output_box->AddText(fit_output_line);
    std::sprintf(fit_output_line, "Edm = %.6g", ppm_fit_values->Edm());
    fit_output_box->AddText(fit_output_line);
    std::sprintf(fit_output_line, "NCalls = %u", ppm_fit_values->NCalls());
    fit_output_box->AddText(fit_output_line);
    fit_output_box->Draw();

    if (save_graphs) {
        char output_filename[256];
        std::sprintf(output_filename, "scan_histogram_%s.png", run_timestamp);
        c1->SaveAs(output_filename);
    }



    // start of output block


    // Output the already-normalized parameters.
    double he_ppm = normalized_params[0]; double ar_ppm = normalized_params[1]; double o2_ppm = normalized_params[2]; double n2_ppm = normalized_params[3]; double co2_ppm = normalized_params[4]; double ch4_ppm = normalized_params[5];
    std::cout << he_ppm << " " << ar_ppm << " " << o2_ppm << " " << n2_ppm << " " << co2_ppm << " " << ch4_ppm << std::endl;

    // end of output block




    return 0; // Successful execution
}



/// to compile type:
///   g++ spectre_to_ppm_converter_th1d_fit_chi2_test.C $(root-config --glibs --cflags --libs) -o spectre_to_ppm_converter_chi2_test


/// to execute via Python3:
///   CSV_concentrations = subprocess.run(["input_test",comma-separated-arguements],capture_output=True,cwd=cwd)
///   #cwd parsed by Python from Config file. All arguements (script name and ints/floats) are provided as list

