{
  gROOT->ProcessLine(".x plotscan.C"); //defines and scales templates

  gStyle->SetOptStat(0);
  TH1F hdata2("hdata2","",50,0.5,50.5); // Throughout we need to find a way to not hardcode the mass count and bin number
  hdata2.GetXaxis()->SetTitle("m/e");
  hdata2.GetYaxis()->SetTitle("P (mbar)");
  hdata2.SetTitle("Doe Canyon sample"); //GK COMMENT: graph name should not be hardcoded here!!!

  //use EM for values less than 200 ppm otherwise use Faraday Cup
  //faraday measurement, uncert = 30 ppm + 10% of reading; 200 ppm = 0.2 mbar
  //EM measurement, uncert = 0.4 ppm + 10% of reading
  Int_t j;
  TScan co2gas; co2gas.ReadPeaks("cgas-fc-000010_peaks.dat");
  for(j=1;j<50;j++)
    {
      if (co2gas.GetPeak(j) > 0 ){ if (j!=12 && j!=13 && j!=30) {hdata2.SetBinContent(j, co2gas.GetPeak(j)); hdata2.SetBinError(j, co2gas.GetPeakU(j) ); }}
    }

  hdata2.SetMarkerStyle(20);

  //run the fit

  gROOT->ProcessLine(".L fitfn.C"); //references the fitfn.C code for use
  TF1 ffit("ffit",fitfn,1,49,10); //creates a 1D function named ffit based on the code of fitfn.C and passes arguments for the min value (1) max value (49) and number of parameters (10)

  //Names the ten parameters used in the fitfn.C code for the different peaks/gases
  ffit.SetParName(0,"ppmArgon40");
  ffit.SetParName(1,"ppmAir");
  ffit.SetParName(2,"ppmO2");
  ffit.SetParName(3,"ppmHe");
  ffit.SetParName(4,"ppmCH4");
  ffit.SetParName(5,"ppmCO2");
  ffit.SetParName(6,"ppmN2");
  ffit.SetParName(7,"ppmH2O"); 
  ffit.SetParName(8,"ppmArgon36");
  ffit.SetParName(9,"ppmArgon38");
  
  //GK NOTE: code below sets the parameters for the fitfn.C using the getScale factors of the gas pointers
  
  //  hdata2.SetBinContent(36,0); hdata2.SetBinError(36,0); hdata2.SetBinContent(38,0); hdata2.SetBinError(38,0);
  hdata2.SetBinContent(47,0); hdata2.SetBinError(47,0); //remove bin 47 for now since it's not in the calibration
  ffit.SetParameter(0, p40Ar.GetScale() );
  ffit.SetParameter(1, pAir.GetScale() ); ffit.SetParLimits(1, 0, pAir.GetScale()* 10);
  ffit.SetParameter(2, pO2.GetScale() );
  ffit.SetParameter(3, pHe.GetScale() );
  ffit.SetParameter(4, pCH4.GetScale() );
  ffit.SetParameter(5, pCO2.GetScale() );
  ffit.SetParameter(6, pN2.GetScale() );
  ffit.SetParameter(7, pH2O.GetScale() );
  ffit.SetParameter(8, p36Ar.GetScale() );
  ffit.SetParameter(9, p38Ar.GetScale() );

  ffit.FixParameter(1,0);
    //ffit.FixParameter(8,0);
    //ffit.FixParameter(9,0);
    //  ffit.FixParameter(6,10000);
    //ffit.FixParameter(2, 0); //fix O2/N2 to zero since we are fitting air
    //ffit.FixParameter(6, 0 );

  hdata2.Fit("ffit","R0S"); //HERE IS THE FITTING COMMAND I THINK, data is fitted to histogram hdata2 using the function ffit !!!!!!!!!!!!!!!!!!!!!!!!!!!
  //(I THINK THIS IS TRUE BUT NOT POSITIVE) In the above command R0S indicates R:use range defined by ffit instead of full range of hdata2, 0:zero indicates not to immediatly plot the data and S:means result and returns a TFitResultPtr 

  //plot the data and the stacked template histograms
  TCanvas c2("c2","",640,480); c2.Draw();
  TPad pleft("pleft","",0.01,0.01,0.7,0.99);
  TPad pright("pright","",0.7,0.01,0.99,0.99);
  pleft.Draw();
  pright.Draw();
  pleft.cd();
  pleft.SetLogy();

  THStack *hs1 = new THStack("hs1","Stacked; m/e; P");
  TH1F hArgon40("hArgon40","",50,0.5,50.5);
  TH1F hArgon36("hArgon36","",50,0.5,50.5);
  TH1F hArgon38("hArgon38","",50,0.5,50.5);
  TH1F hArgonsum("hArgonsum","",50,0.5,50.5);
  TH1F hO21("hO21","",50,0.5,50.5);
  TH1F hHe1("hHe1","",50,0.5,50.5);
  TH1F hCH41("hCH41","",50,0.5,50.5);
  TH1F hCO21("hCO21","",50,0.5,50.5);
  TH1F hN21("hN21","",50,0.5,50.5);
  TH1F hH2O1("hH2O1","",50,0.5,50.5);
  TH1F hAir1("hAir1","",50,0.5,50.5);

  //code below cycles through mass 1 through 50 and assigns the (I think scaled/fitted???) peak values pointed to by pO2 etc in the associated bins of hO21 etc)
  for(j=1; j<50; j++){hArgonsum.SetBinContent(j, p40Ar.GetPeak(j) + p36Ar.GetPeak(j) + p38Ar.GetPeak(j)); }
  for(j=1; j<50; j++){hO21.SetBinContent(j, pO2.GetPeak(j) ); }
  for(j=1; j<50; j++){hHe1.SetBinContent(j, pHe.GetPeak(j) ); }
  for(j=1; j<50; j++){hCH41.SetBinContent(j, pCH4.GetPeak(j) ); }
  for(j=1; j<50; j++){hCO21.SetBinContent(j, pCO2.GetPeak(j) ); }
  for(j=1; j<50; j++){hN21.SetBinContent(j, pN2.GetPeak(j) ); }
  for(j=1; j<50; j++){hH2O1.SetBinContent(j, pH2O.GetPeak(j) ); }
  for(j=1; j<50; j++){hAir1.SetBinContent(j, pAir.GetPeak(j) ); }

  hArgonsum.SetFillColor(kRed); hArgonsum.SetLineColor(kRed); 
  hO21.SetFillColor(kBlue); hO21.SetLineColor(kBlue);
  hHe1.SetFillColor(kGreen); hHe1.SetLineColor(kGreen);
  hCH41.SetFillColor(38); hCH41.SetLineColor(38);
  hCO21.SetFillColor(kOrange);  hCO21.SetLineColor(kOrange);
  hN21.SetFillColor(613); hN21.SetLineColor(613);
  hH2O1.SetFillColor(kYellow); hH2O1.SetLineColor(kYellow);
  hAir1.SetFillColor(kCyan-3); hAir1.SetLineColor(kCyan-3);
  
  hs1->Add( &hAir1 );
  hs1->Add( &hArgonsum );
  hs1->Add( &hO21 );
  hs1->Add( &hHe1 );
  hs1->Add( &hCH41 );
  hs1->Add( &hN21 );
  hs1->Add( &hCO21 );
  hs1->Add( &hH2O1 );
   
  hdata2.Draw("e1p");
  hs1->Draw("BAR1,same");
  hdata2.Draw("e1p,same");

  TLegend ll1(0.135,0.501,0.284,0.869);
  ll1.SetBorderSize(0);
  ll1.AddEntry( &hArgon,"argon");
  ll1.AddEntry( &hO21,"oxygen");
  ll1.AddEntry( &hHe1,"helium");
  ll1.AddEntry( &hCH41,"methane");
  ll1.AddEntry( &hN21, "nitrogen");
  ll1.AddEntry( &hCO21,"carbon dioxide");
  ll1.AddEntry( &hH2O1,"water");
  ll1.AddEntry( &hAir1,"air");
  ll1.Draw();

  pright.cd();
  TPaveText pt(0.,0.1,1,0.9);
  pt.SetFillColor(kWhite);
  pt.SetBorderSize(0);
  pt.SetTextAlign(12);
  char pttext[256];
  TDatime dd;

  //NOTE ALL OF THIS SHOULD NOT BE HARDCODED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  pt.AddText("Carleton Gas Analysis System CGAS\n");
  sprintf(pttext,"Result Generated %2i/%2i/%4i %02i:%02i\n",dd.GetDay(), dd.GetMonth(), dd.GetYear(), dd.GetHour(), dd.GetMinute()); pt.AddText(pttext);
  pt.AddText("Sample ID 005");
  pt.AddText("Sample Line 05");
  pt.AddText("Sample Time 06/12/2025 11:04");
  pt.AddText("Calibration Scan 1: 002, 04/12/2025, grade 5 argon");
  pt.AddText("Calibration Scan 2: 003, 06/12/2025, CO2 calibration standard");
  pt.AddText("Sample comment: Doe Canyon gas after Air Products");
  //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  pt.AddText("");

  sprintf(pttext,"argon40  = %.1f +/- %.1f (ppm) \n",ffit.GetParameter(0), ffit.GetParError(0)); pt.AddText(pttext);
  sprintf(pttext,"argon36  = %.1f +/- %.1f (ppm) \n",ffit.GetParameter(8), ffit.GetParError(8)); pt.AddText(pttext);
  sprintf(pttext,"argon38  = %.1f +/- %.1f (ppm) \n",ffit.GetParameter(9), ffit.GetParError(9)); pt.AddText(pttext);
  sprintf(pttext,"air      = %.1f +/- %.1f (ppm) \n",ffit.GetParameter(1), ffit.GetParError(1)); pt.AddText(pttext);
  sprintf(pttext,"oxygen   = %.1f +/- %.1f (ppm) [fixed] \n",ffit.GetParameter(2), ffit.GetParError(2)); pt.AddText(pttext);
  sprintf(pttext,"nitrogen = %.1f +/- %.1f (ppm) [fixed] \n",ffit.GetParameter(6), ffit.GetParError(6)); pt.AddText(pttext);
  sprintf(pttext,"helium   = %.1f +/- %.1f (ppm) \n",ffit.GetParameter(3), ffit.GetParError(3)); pt.AddText(pttext);
  sprintf(pttext,"methane  = %.1f +/- %.1f (ppm) \n",ffit.GetParameter(4), ffit.GetParError(4)); pt.AddText(pttext);
  sprintf(pttext,"water    = %.1f +/- %.1f (ppm) \n",ffit.GetParameter(7), ffit.GetParError(7)); pt.AddText(pttext);  
  sprintf(pttext,"CO2      = balance\n"); pt.AddText( pttext );


 pt.Draw();
 

  
}
