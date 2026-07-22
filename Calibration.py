from ConvertCsvScanToList import read_em_fc_combined
import JSONoperators
import json
from SpectraInterpreter import solve_mass_spectrum_ROOT

def Calibration():

    initial_mass = 1
    step = 1
    amount_of_steps = 50

    cgas000108 = [0] + read_em_fc_combined("000108",initial_mass,step,amount_of_steps) #95% CO2 w. 1% of methane, helium, N2, O2, Ar
    cgas000107 = [0] + read_em_fc_combined("000107",initial_mass,step,amount_of_steps) # 100% CO2
    cgas000105 = [0] + read_em_fc_combined("000105",initial_mass,step,amount_of_steps) #95% Ar w. 1% of methane, helium, N2, O2, CO2
    cgas000084 = [0] + read_em_fc_combined("000084",initial_mass,step,amount_of_steps) # 100% N2


    coefficients = {}

    coefficients["He_4"] = cgas000105[4] / 0.01
    coefficients["CO2_44"] = cgas000105[44] / 0.01

    coefficients["Ar_40"] = ((cgas000105[4] / cgas000108[4] ) * cgas000108[40] ) / 0.01
    coefficients["Ar_38"] = ((cgas000105[4] / cgas000108[4] ) * cgas000108[38] ) / 0.01
    coefficients["Ar_36"] = ((cgas000105[4] / cgas000108[4] ) * cgas000108[36] ) / 0.01

    coefficients["O2_32"] = cgas000105[32]  / 0.01
    coefficients["CH4_15"] = cgas000105[15]  / 0.01

    coefficients["CO2_28"] = coefficients["CO2_44"] * ( cgas000107[28]  / cgas000107[44] )
    coefficients["CO2_29"] = coefficients["CO2_44"] * ( cgas000107[29]  / cgas000107[44] )

    coefficients["N2_28"] = (cgas000105[28]  / 0.01 )  - coefficients["CO2_28"]
    coefficients["N2_29"] = ( 2*0.0038/(1-2*0.0038)) * coefficients["N2_28"]


    coefficients["N2_14"] = (cgas000084[14] / cgas000084[28])*coefficients["N2_28"]
    coefficients["N2_15"] = ( 0.0038/(1-0.0038))*coefficients["N2_14"]
    #coefficients["N2_15"] = (cgas000084[15] / cgas000084[28])*coefficients["N2_28"]



    return(coefficients)




if __name__ == "__main__":
    new_parameters = Calibration()
    config_line = JSONoperators.ReadJSONConfig("cracking_patterns")
    config_line["list"] = new_parameters
    config_string = json.dumps(config_line)
    print(config_string)
    JSONoperators.EditJSONConfig("cracking_patterns",config_string)


    scan = read_em_fc_combined("000108",1,1,50)
    print(solve_mass_spectrum_ROOT(scan,1,1))

    scan = read_em_fc_combined("000105",1,1,50)
    print(solve_mass_spectrum_ROOT(scan,1,1))

    scan = read_em_fc_combined("000084",1,1,50)
    print(solve_mass_spectrum_ROOT(scan,1,1))