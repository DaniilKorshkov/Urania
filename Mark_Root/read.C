{
  gStyle->SetOptStat(0);
  Int_t run = 36;
  Int_t nscans, i;
  char fname[256]; sprintf(fname,"cgas-em-%06i.txt",run);
  printf("reading %s\n", fname);
  FILE *fin = fopen(fname,"read");
  sprintf(fname,"cgas-fc-%06i-peaks.dat",run);
  FILE *fout = fopen(fname,"write");
  Float_t m;
  fscanf(fin,"%i",&nscans);
  printf("nscans=%i\n",nscans);
  Float_t xx[10000], yy[10000];
  Int_t j=0,nentries=0;
  //scanf string
  TString scanstring="%f";
  for(i=0;i<nscans;i++){scanstring+=" %f";};
  Float_t rin[10];
  Float_t ravg;
  
  while (fscanf(fin,"%f", &m ) > 0 )
    {
      for(j=0;j<nscans;j++){fscanf(fin,"%f",&rin[j]); }
      ravg=0; for(i=0;i<nscans;i++){ ravg+= rin[i]; } ravg /= (Float_t)nscans;
      printf("%f %f\n",m, ravg);
      xx[nentries] = m;
      yy[nentries] = ravg;
      nentries++;
    }

  TGraph gg(nentries,xx,yy);
  Float_t m;
  TF1 fg("fg","gaus");
  fg.SetParameters(1,0.5,1);

  TH1F mpeaks("mpeaks","",50,0.5,50.5);

  for(m=1; m<50; m++)
    {
      fg.SetRange(m-0.5,m+0.25);
      fg.SetParameter(1, m); fg.SetParameter(0,1); fg.SetParameter(2,0.5);
      TFitResult b = gg.Fit("fg","R");
      printf("minuit status = %i\n", gMinuit->GetStatus() );
      if ( !strncmp(gMinuit->fCstatu.Data(),"CONVERGED",9) ){
	if ( fg.GetParameter(0) > 0.01 && (fg.GetParError(0)/fg.GetParameter(0)) < 0.25 && fabs( fg.GetParameter(1)-m) < 0.3 ){
	  printf("mass %i %f +/- %f\n", (Int_t)m, fg.GetParameter(0), fg.GetParError(0) );
	  fprintf(fout,"%i %f %f\n", m, fg.GetParameter(0), fg.GetParError(0) );
          mpeaks.SetBinContent( (Int_t)m, fg.GetParameter(0) );
	  mpeaks.SetBinError( (Int_t)m, fg.GetParError(0) );
	}
      }
      else printf("gMinuit failed\n");
    }

  fclose(fin);
  fclose(fout);

  TFile fout2("scan_36.root","RECREATE");
  TH2F hh2("hh2","",100,0,50,100,1e-4,1000);
  hh2.GetXaxis()->SetTitle("m/e");
 
  hh2.Draw();
  gg.Draw("pl");
  mpeaks.Draw("ep,same");
  mpeaks.SetMarkerStyle(20);
  fout2.cd();
  gg.Write("gg");
  mpeaks.Write();
  fout2.Close();

}
