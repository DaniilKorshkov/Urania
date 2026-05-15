#include "TScan.h" //Include the header file here containing variable declarations etc

TScan::TScan()
{
//NOTE these variables are declared as pointers in the private section of the header file "TArrayF *fEM, *fEMU, *fFC, *fFCU;"
fEM = new TArrayF(50); //creates fEM as an array of 50 32-bit floats, "new" stores them as pointers on the heap and they will need to be deleted to remove them!!! 
fEMU = new TArrayF(50);
fFC= new TArrayF(50);
fFCU = new TArrayF(50);
Int_t i;
for(i=0; i<50; i++){fEM->SetAt(0,i); } //set the i'th entry if tge fEM array to equal 0
for(i=0; i<50; i++){fFC->SetAt(0,i); } //set the i'th entry if tge fFC array to equal 0
fScale=1;
}
TScan::~TScan()
{
delete fEM; fEM=0;
delete fEMU; fEMU=0;
}

void TScan::SetEM(Int_t m, Float_t p, Float_t ep) //set Electron Multiplier to have three columns for mass, pressure and error_pressure
{
fEM->SetAt(p,m); //set the m'th entry in the array fEM to be the value p ???
fEMU->SetAt(ep,m); //set the m'th entry in the array fEMU to be the value ep ???
}
void TScan::SetFC(Int_t m, Float_t p, Float_t ep) //set Faraday Cup to have three columns for mass, pressure and error_pressure
{
fFC->SetAt(p,m); //set the m'th entry in the array fFC to be the value p ???
fFCU->SetAt(ep,m); //set the m'th entry in the array fFCU to be the value p ???
}
Float_t TScan::GetScale(){ return fScale; }
void TScan::SetScale(Float_t f){ fScale=f; }

void TScan::AddComponent( TScan *aScan, Float_t fraction) //add elements to an array by iterating through a series of individual scans called aScan
{
Int_t j; //creates integer variable j for cycling through masses in a scan
for(j=0;j<50;j++) //for loop iterating through the 50 mass entries in a scan
  {
if ( aScan->HasPeak(j) ) AddPeak(j, aScan->GetPeak(j)*fraction, aScan->GetPeakU(j)*fraction ); //checks if a peak exists at mass j, and if it does exist it gets the peak value 
}
}

Float_t TScan::GetEM(Int_t m)
{
return fEM->GetAt(m);
}
Float_t TScan::GetEMU(Int_t m)
{
return fEMU->GetAt(m);
}
Float_t TScan::GetFC(Int_t m)
{
return fFC->GetAt(m);
}
Float_t TScan::GetFCU(Int_t m)
{
return fFCU->GetAt(m);
}
void TScan::SetIsPattern(Bool_t isP, (const char *)pattern)
{
fIsPattern = isP;
//fPattern = pattern;
}
Bool_t TScan::HasPeak(Int_t m)
{
if (GetFC(m) > -9998 || GetEM(m) > -9998 ) return kTRUE; 
//If the peak at mass m was not detected/scanned the code returns -9999, therefore if the return is greater than -9998, the peak was scanned and the return is true
//note here "||" is the boolean OR operator, so if the mass was scanned with either the faraday cup or the multiplier the return will be true
 else return kFALSE;
//If the peak return is less than -9998 than the return is false and the peak was not scanned
}

Float_t TScan::GetPeak(Int_t m){
if (GetEM(m) < 200 ) return GetEM(m)*GetScale(); //if the detected ppm is below 200 the electron multiplier value is used
 else if (GetFC(m) > 0 ) return GetFC(m)*GetScale(); //if the detected ppm is above 200 and the faraday detector is above 0 then the faraday cup value is used for the mass
 else return -9999; // return if the peak at mass m is not in the range scanned
}

Float_t TScan::GetPeakU(Int_t m){
if ( GetEM(m) < 200 ) return GetEMU(m)*GetScale();
 else if ( GetFC(m) > 0) return GetFCU(m)*GetScale();
 else return -9999;
}

void TScan::SetPeak(Int_t m, Float_t val, Float_t valu)
{
if ( val < 200.) SetEM(m,val,valu);
 else SetFC(m,val,valu);

}
void TScan::AddPeak(Int_t m, Float_t val, Float_t valu)
{
Float_t oldval = GetPeak(m); if (oldval < 0 ) oldval = 0;
Float_t oldvalu = GetPeakU(m); if (oldvalu < 0) oldvalu = 0;

Float_t newval = val + oldval;
Float_t newu = sqrt(oldvalu*oldvalu + valu*valu);
SetPeak(m, newval,newu);

}
