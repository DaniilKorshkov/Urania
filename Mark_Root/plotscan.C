{ //THIS WHOLE FILE IS TO CREATE A TEMPLATE FOR FITTING DATA TO WITH SCANFIT.C !!!!!!!!!!!!!!
  gROOT->ProcessLine(".x patterns.C"); //runs patterns.C macro

  //following scale factors from the CO2 calibration bottle with corrections to match data (NOTE FROM GRAHAM, WHY IS THIS HARD CODED? IT MUST HAVE COME FROM OTHER CALCULATIONS OF THE KNOWN CALIBRATED GAS BOTTLES)
  pArgon.SetScale(0.00999*1000); //no correction, pressures calibrated to argon
  pO2.SetScale(0.01*1000 * 0.7 * 0.72 ); //correction is 0.7*0.72;
  pHe.SetScale(0.00999*1000*0.14/1.2); //correction is 0.14/0.12
  pCH4.SetScale(0.00999*1000 * 1.4/1.2); //correction is 1.4/1.2
  pCO2.SetScale(0.96*1000/(1+0.114+0.085)*620./800.); //correction is 620/800
  pN2.SetScale(0.01*1000); //no correction applied for N2

  TH1F hh1("hh1","",50,0.5,50.5); 
  //TH1F is a histogram (named hh1, with an empty title "") with one float per channel. Maximum precision 7 digits, maximum integer bin content = +/-16777216
  // Range on x-axis is from 0.5 to 50.5, and with a total of 50 bins
  //2^24 = 16777216 is the maximum integer that can be properly represented by a float32 with 23-bit mantissa
  hh1.SetTitle("CO2 calibration gas");//Title of hh1 is set here instead of in the previous command for some reason?

  //j is a generic integer established for the loop, i.e. j will vary from 1 to 50 to get data from each mass
  Int_t j;

  //loop varying generic integer j from 1 to 50 while increasing j by +1 with each iteration, used to load peak data from each mass from mass 1 to mass 50???????????????
  for(j=1; j<50; j++)
    {
      hh1.SetBinContent(j, (Double_t)pArgon.GetPeak(j)+(Double_t)pO2.GetPeak(j)+(Double_t)pHe.GetPeak(j)+(Double_t)pCH4.GetPeak(j)+(Double_t)pCO2.GetPeak(j)+(Double_t)pN2.GetPeak(j) );
    }

  gStyle->SetOptStat(0);
  TH1F hdata("hdata","",50,0.5,50.5);

  //use EM for values less than 200 ppm otherwise use Faraday Cup
  //faraday measurement, uncert = 30 ppm + 10% of reading; 200 ppm = 0.2 mbar
  //EM measurement, uncert = 0.4 ppm + 10% of reading

  //following data values read from the CO2 calibration bottle scans (NOTE FROM GRAHAM: THIS SEEMS TO BE USING SAMPLE BOTTLE DATA TO GENERATE A BASE FRAMEWORK FOR SAVING DATA PROCESSED BY SCANFIT.C)
  hdata.SetBinContent(4, 1.2); hdata.SetBinError(4, 0.03+0.1*1.2); 
  hdata.SetBinContent(15,6); hdata.SetBinError(15,0.03+0.1*6);
  hdata.SetBinContent(16,60); hdata.SetBinError(16,0.03+0.1*60);//note here 0.03 is used due to the Faraday Cup
  hdata.SetBinContent(17,0.18); hdata.SetBinError(17,4e-4+0.1*0.18);//note here 4e-4 is used due to Electron Multiplier
  hdata.SetBinContent(18,0.27); hdata.SetBinError(18,0.03+0.1*0.27);
  hdata.SetBinContent(28,75); hdata.SetBinError(28,0.03+0.1*0.75);//*********here I think there is an error, the value is set to (75), but the 10% of reading uses (0.1*0.75)***********
  hdata.SetBinContent(29,0.73); hdata.SetBinError(29,4e-4+0.1*0.73);
  hdata.SetBinContent(32,5); hdata.SetBinError(32,0.03+0.1*5);
  hdata.SetBinContent(34,0.02); hdata.SetBinError(34,4e-4+0.1*0.02);
  hdata.SetBinContent(36,0.023); hdata.SetBinError(36,4e-4+0.1*0.023);
  hdata.SetBinContent(38,0.0045); hdata.SetBinError(38,4e-4+0.1*0.0045);
  hdata.SetBinContent(40,10); hdata.SetBinError(40,0.03+0.1*10);
  hdata.SetBinContent(44,620);hdata.SetBinError(44,0.03+0.1*620);
  hdata.SetBinContent(45,6); hdata.SetBinError(45,0.03+0.1*6);
  hdata.SetBinContent(46,2); hdata.SetBinError(46,0.03+0.1*2);
  hdata.SetBinContent(47,0.02); hdata.SetBinError(47,4e-4+0.1*0.02);
  //The data above set the value and the error of each of the mass bins associated with any of the 6 main gases being looked for in the spectrum based on the patterns.C cracking patterns
  //This seems to populate the histogram with calibration data??? Based on what???

  hdata.SetMarkerStyle(20);

  //plot the data and the stacked template histograms
  hh1.Draw();
  hh1.GetXaxis()->SetTitle("m/e");
  hh1.GetYaxis()->SetTitle("P (mbar)");

  THStack *hs = new THStack("hs","Stacked; m/e; P"); //Generate stacked data in the bins of the histogram hh1 to have multiple gases separated in each bin
  TH1F hArgon("hArgon","",50,0.5,50.5); //Creates histogram float dataset for Argon from 0.5 to 50.5 divided into 50 bins
  TH1F hO2("hO2", "", 50, 0.5, 50.5);   //Creates histogram float dataset for O2 from 0.5 to 50.5 divided into 50 bins
  TH1F hHe("hHe","",50,0.5,50.5);       //Creates histogram float dataset for He from 0.5 to 50.5 divided into 50 bins
  TH1F hCH4("hCH4","",50,0.5,50.5);     //Creates histogram float dataset for CH4 from 0.5 to 50.5 divided into 50 bins
  TH1F hCO2("hCO2","",50,0.5,50.5);     //Creates histogram float dataset for CO2 from 0.5 to 50.5 divided into 50 bins
  TH1F hN2("hN2","",50,0.5,50.5);       //Creates histogram float dataset for N2 from 0.5 to 50.5 divided into 50 bins

  for(j=1; j<50; j++){hArgon.SetBinContent(j, pArgon.GetPeak(j) ); } //loads data pointed to by pArgon for each mass peak from 1 to 50 generated by TScan and the patterns from patterns.C
  for (j = 1; j < 50; j++) { hO2.SetBinContent(j, pO2.GetPeak(j)); } //loads data pointed to by pO2 for each mass peak from 1 to 50 generated by TScan and the patterns from patterns.C
  for(j=1; j<50; j++){hHe.SetBinContent(j, pHe.GetPeak(j) ); }       //loads data pointed to by pHe for each mass peak from 1 to 50 generated by TScan and the patterns from patterns.C
  for(j=1; j<50; j++){hCH4.SetBinContent(j, pCH4.GetPeak(j) ); }     //loads data pointed to by pCH4 for each mass peak from 1 to 50 generated by TScan and the patterns from patterns.C
  for(j=1; j<50; j++){hCO2.SetBinContent(j, pCO2.GetPeak(j) ); }     //loads data pointed to by pCO2 for each mass peak from 1 to 50 generated by TScan and the patterns from patterns.C
  for(j=1; j<50; j++){hN2.SetBinContent(j, pN2.GetPeak(j) ); }       //loads data pointed to by pN2 for each mass peak from 1 to 50 generated by TScan and the patterns from patterns.C

  //Sets the colors of the bin data for each gas
  hArgon.SetFillColor(kRed); hArgon.SetLineColor(kRed); 
  hO2.SetFillColor(kBlue); hO2.SetLineColor(kBlue);
  hHe.SetFillColor(kGreen); hHe.SetLineColor(kGreen);
  hCH4.SetFillColor(38); hCH4.SetLineColor(38);
  hCO2.SetFillColor(kOrange);  hCO2.SetLineColor(kOrange);
  hN2.SetFillColor(613); hN2.SetLineColor(613);

  //Adds the datasets of all relevent gases/contaminants to the histogram bins
  hs->Add( &hArgon );
  hs->Add( &hO2 );
  hs->Add( &hHe );
  hs->Add( &hCH4 );
  hs->Add( &hN2 );
  hs->Add( &hCO2 );

  //draws histogram data
  hs->Draw("BAR1,same");
  hdata.Draw("e1p,same");

  //Adds entries in the legend for all relevent gases/contaminants
  TLegend ll(0.1,0.5,0.3,0.9);
  ll.SetBorderSize(0);
  ll.AddEntry( &hArgon,"argon");
  ll.AddEntry( &hO2,"oxygen");
  ll.AddEntry( &hHe,"helium");
  ll.AddEntry( &hCH4,"methane");
  ll.AddEntry( &hN2, "nitrogen");
  ll.AddEntry( &hCO2,"carbon dioxide");
 
  //draws legend
  ll.Draw();

}

