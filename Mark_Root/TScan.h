//Root libraries being called

#include "TH1.h"     //histogram header file from ROOT library
#include "TObject.h" //The TObject class provides default behaviour and protocol for all objects in the ROOT system.
#include "TArray.h"  //Abstract array base class. Used in various types of TArray objects and TH1 histograms in ROOT.

//Header file containing declarations of the descriptions of the logic used by TScan.cc (logic file)
//Header files simply let the compiler know that the functions from those headers are written in other files and what types those functions take in and return
//The point of the header files is to let the source file know the functions exists without having to implement them
class TScan : public TObject
{
 public://calls the TScan.cc (program logic file) program to extract data from datafiles
	 TScan();
	 ~TScan(); // ~TScan is a destructor operator of TScan which essentially deletes TScan from memory to free up computation space, ~object destroys object

  //void is a generic pointer to any datatype with no return value

  //Here EM is the electron multiplier and FC is the faraday cup
	 void SetEM(Int_t m, Float_t p, Float_t ep); 
	 //This is a setter, populated with parameters m, p (pointer to the pressure) and ep (pointer to error of pressure?) where m is an integer value of mass 
	 void SetFC(Int_t m, Float_t p, Float_t ep);

	 void AddComponent( TScan *aScan, Float_t fraction); //*aScan is a specific instance of TScan, and fraction is a parameter
  
  //In ROOT Float_t is a float with 4 bytes of data instead of the builtin basic type float, similarly for Int_t, this type guarantees 32 bit float across all systems preserving legacy compatibility
  //In ROOT float16_t will store the value as a 16bit structure to save storage space, but still uses a 32 bit structure in memory to preserve accuracy during calculations
	 Float_t GetEM(Int_t m); //these are getter statements which obtain the value (in this case of "Int_t m") as a Float_t structure
	 Float_t GetEMU(Int_t m);
	 Float_t GetFC(Int_t m);
	 Float_t GetFCU(Int_t m);
	 Float_t GetPeak(Int_t m);
	 Float_t GetPeakU(Int_t m);
	 Float_t GetScale();

	 void SetPeak(Int_t m, Float_t val, Float_t valu=0);
	 void AddPeak(Int_t m, Float_t val, Float_t valu=0);
	 //In ROOT Bool_t is a boolean with 0=false and 1=true, uses a fixed size of 4 bytes compared to a standard 1 byte to ensure compatibility across legacy systems (32-bit, 64-bit, ARM vs Intel etc...)
	 void SetIsPattern(Bool_t isP, (const char *)pattern); 
	 void SetScale( Float_t f); 
	 Bool_t HasPeak(Int_t m);


 private:
	 //"*" is a Pointer Declaration: Defines a variable that holds the memory address of a ROOT object (e.g., TH1F *h1 = new TH1F(...))
	 TArrayF *fEM, *fEMU, *fFC, *fFCU; //fEM(5), fEMU(5), fFC(50), fFCU(50);
	 time_t fTimeEM, fTimeFC;
	 Bool_t fIsPattern;
	 TString fPattern;
	 Float_t fScale;
};

