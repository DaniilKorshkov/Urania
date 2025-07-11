def CalculateMassSpan():


    isotope_table = {

    "H":{ "1":0.99985,"2":0.00015},
    "He":{"4":1.0},
    "C":{"12":0.9884,"13":0.0116  },
    "N":{"14":0.99578,"15":0.00422},
    "O":{"16":0.99738,"17":0.000367,"18":0.002253},
    "Ar":{"36":0.0034,"38":0.0006,"40":0.996}
    
    }


    product = {"0":1}

    MoleculeStructure, charge = get_input()
    

    for key in MoleculeStructure:


        for i in range(MoleculeStructure[key]):
            product = AddAtomToPreviousMolecule(product,isotope_table[key])


    
    product_wrt_charge = {}

    for key in product:
        if int(int(key)/charge) == float(int(key)/charge):
            product_wrt_charge[int(key)/charge] = product[key]

    
    return product_wrt_charge
        




def AddAtomToPreviousMolecule(molecule, atom):

    new_molecule = {}
    for atom_key in atom:

        
        for molecule_key in molecule:
            new_molecule_key = str(int(molecule_key) + int(atom_key))
            try:
                new_molecule[new_molecule_key] += molecule[molecule_key]*atom[atom_key]
                
            except:
                new_molecule[new_molecule_key] = molecule[molecule_key]*atom[atom_key]
    
    return(new_molecule)


def get_input():
    empty_molecule_structure = { "H":0, "He":0, "C":0, "N":0, "O":0, "Ar":0  }
    for key in empty_molecule_structure:
        while True:
            try:
                value = int(input(f"{key}: "))
                assert value >= 0
                empty_molecule_structure[key] = value
                break
            except:
                print("Bad input")
    
    while True:
            try:
                charge = int(input(f"Charge of this particle: "))
                assert charge > 0
                break
            except:
                print("Bad input")
    
    return empty_molecule_structure, charge




def CalculateCrackingPattern():

    cracking_pattern = [0]*50

    while True:
        print("Enter molecular formula for child particle: ")
        child_molecule_isotopes = CalculateMassSpan()
        try:
            while True:
                main_peak_height = float(input("Main Peak Height for this child particle (raw electric curent): "))
                assert main_peak_height >= 0
                break
        except:
            print("Bad input")



        child_molecule_list = []         
        for key in child_molecule_isotopes:
            if int(key) <= 50:
                child_molecule_list.append(child_molecule_isotopes[key])

            
        multiplication_factor = main_peak_height / (max(child_molecule_list))

        for key in child_molecule_isotopes:
            if int(key) <= 50:
                cracking_pattern[ int(key)-1 ] += child_molecule_isotopes[key]*multiplication_factor
            

        repeat = str(input("More child particles (y/n)?: "))
        if repeat[0].lower() == "n":
            break
    
    while True:
        try:
            concentration = float(input("concentration of this compound (fraction from 0 to 1): "))
            assert concentration > 0
            assert concentration <= 1
            break
        except:
            print("Bad input")

    
    cracking_pattern_wrt_concentration = []
    for element in cracking_pattern:
        cracking_pattern_wrt_concentration.append( element/concentration )

    return cracking_pattern_wrt_concentration



            


            












if __name__ == "__main__":
    print(CalculateCrackingPattern())