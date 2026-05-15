Double_t fitfn(Double_t *x, Double_t *par)
{
  Double_t arg=0;
  Double_t m = x[0];
  Int_t j = (Int_t)m;
  p40Ar.SetScale(par[0]);
  pAir.SetScale(par[1]);
  pO2.SetScale(par[2]);
  pHe.SetScale(par[3]);
  pCH4.SetScale(par[4]);
  pCO2.SetScale(par[5]);
  pN2.SetScale(par[6]);
  pH2O.SetScale(par[7]);  
  p36Ar.SetScale(par[8]);
  p38Ar.SetScale(par[9]);

  Double_t val = (Double_t)p40Ar.GetPeak(j)+(Double_t)pO2.GetPeak(j)+(Double_t)pHe.GetPeak(j)+(Double_t)pCH4.GetPeak(j)+(Double_t)pCO2.GetPeak(j)+(Double_t)pN2.GetPeak(j)+pH2O.GetPeak(j)+pAir.GetPeak(j)+p36Ar.GetPeak(j)+p38Ar.GetPeak(j);
   
  return val;
}
