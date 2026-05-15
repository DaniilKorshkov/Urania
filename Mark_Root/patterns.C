{
  gROOT->ProcessLine(".L TScan.cc"); //runs TScan.cc macro

  //define cracking patterns, p indicates pointers to variables in memory from TScan
  TScan pCO2, pCO, pO2, pN2, pHe, pCH4, pH2O, pAir, p36Ar, p38Ar, p40Ar, pArgon;
  pCO2.SetIsPattern(kTRUE, "CO2"); pCO2.SetPeak(44,1); pCO2.SetPeak(28,0.114); pCO2.SetPeak(29,0.114*0.01); pCO2.SetPeak(16,0.085);
  pCO.SetIsPattern(kTRUE,"CO"); pCO.SetPeak(28,1); pCO.SetPeak(12,0.045); pCO.SetPeak(16,0.009);
  pO2.SetIsPattern(kTRUE,"O2"); pO2.SetPeak(32,1); pO2.SetPeak(16,0.114); pO2.SetPeak(34,0.004);
  pN2.SetIsPattern(kTRUE,"N2"); pN2.SetPeak(28,1); pN2.SetPeak(14,0.072); pN2.SetPeak(29,0.008);
  pHe.SetIsPattern(kTRUE,"He"); pHe.SetPeak(4,1);
  pCH4.SetIsPattern(kTRUE,"CH4"); pCH4.SetPeak(16,1); pCH4.SetPeak(15,0.858); pCH4.SetPeak(14,0.156);
  pH2O.SetIsPattern(kTRUE,"H2O"); pH2O.SetPeak(18,1); pH2O.SetPeak(17,0.23); pH2O.SetPeak(16,0.011);
  p36Ar.SetIsPattern(kTRUE,"36Ar"); p36Ar.SetPeak(36,1);
  p38Ar.SetIsPattern(kTRUE,"38Ar"); p38Ar.SetPeak(38,1);
  p40Ar.SetIsPattern(kTRUE,"40Ar"); p40Ar.SetPeak(40,1);

  //combines the values of the three pajor argon isotopes of mass 36, mass 38 and mass 40 to generate the full argon cracking pattern
  pArgon.SetIsPattern(kTRUE,"Argon"); pArgon.AddComponent(&p36Ar,0.00334); pArgon.AddComponent(&p38Ar,0.00063); pArgon.AddComponent(&p40Ar,0.996);

  //combines the paterns of O2, N2 and Ar in there relative contributions in atmospheric air to set the "pattern" for air contamination
  pAir.SetIsPattern(kTRUE,"Air"); pAir.AddComponent( &pO2, 0.2095); pAir.AddComponent(&pN2, 0.7809); pAir.AddComponent(&pArgon,0.0093);

 
}
