import JSONoperators


def ConvertPPMtoIC(ppm_dictionary, raw_coeff = 0.0005):
    ic_dictionary = {}
    coeff_dictionary = JSONoperators.ReadJSONConfig("cracking_patterns","list")
    ic_dictionary["28"] = 0

    RAW_dictionary = {}
    for key in ppm_dictionary:
        RAW_dictionary[key] = ppm_dictionary[key]*raw_coeff


    for key in RAW_dictionary:
        match key:
            case "CO2":
                ic_dictionary["44"] = RAW_dictionary[key]*coeff_dictionary["CO2_44"]
                ic_dictionary["28"] += RAW_dictionary[key]*coeff_dictionary["CO2_28"]
            case "N2":
                ic_dictionary["28"] += RAW_dictionary[key]*coeff_dictionary["N2_28"]
            case "O2":
                ic_dictionary["32"] = RAW_dictionary[key]*coeff_dictionary["O2_32"]
            case "CH4":
                ic_dictionary["15"] = RAW_dictionary[key]*coeff_dictionary["CH4_15"]
            case "He":
                ic_dictionary["4"] = RAW_dictionary[key]*coeff_dictionary["He_4"]
            case "Ar":
                ic_dictionary["40"] = RAW_dictionary[key]*coeff_dictionary["Ar_40"]
            
    
    ic_stdev_dictionary = {}

    for key in ic_dictionary:
        ic_stdev_dictionary[key] = 1900 + ic_dictionary[key]*0.02

    return RAW_dictionary, ic_dictionary, ic_stdev_dictionary


def FindQuadraticError(RAW_dictionary, ppm_dictionary, ic_dictionary, ic_stdev_dictionary, raw_coeff=0.0005):

    ppm_stdev_dictionary = {}
    coeff_dictionary = JSONoperators.ReadJSONConfig("cracking_patterns","list")

    RAW_sum = 1000000*raw_coeff

    print(ic_stdev_dictionary)

    for key in ppm_dictionary:
        ppm_stdev_dictionary[key] = 0
        for error_factor_key in ic_stdev_dictionary:
            

            match key:
                case "CO2":
                    if "44" != error_factor_key:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  RAW_dictionary[key]/RAW_sum**2 ) / (coeff_dictionary["CO2_44"]))**2
                    else:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  (RAW_sum - RAW_dictionary[key])/RAW_sum**2 ) / (coeff_dictionary["CO2_44"]))**2
                case "CH4":
                    if "15" != error_factor_key:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  RAW_dictionary[key]/RAW_sum**2 ) / (coeff_dictionary["CH4_15"]))**2
                    else:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  (RAW_sum - RAW_dictionary[key])/RAW_sum**2 ) / (coeff_dictionary["CH4_15"]))**2
                case "O2":
                    if "32" != error_factor_key:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  RAW_dictionary[key]/RAW_sum**2 ) / (coeff_dictionary["O2_32"]))**2
                    else:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  (RAW_sum - RAW_dictionary[key])/RAW_sum**2 ) / (coeff_dictionary["O2_32"]))**2
                case "N2":
                    if "28" != error_factor_key:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  RAW_dictionary[key]/RAW_sum**2 ) / (coeff_dictionary["N2_28"]))**2
                    else:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  (RAW_sum - RAW_dictionary[key])/RAW_sum**2 ) / (coeff_dictionary["N2_28"]))**2
                case "Ar":
                    if "40" != error_factor_key:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  RAW_dictionary[key]/RAW_sum**2 ) / (coeff_dictionary["Ar_40"]))**2
                    else:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  (RAW_sum - RAW_dictionary[key])/RAW_sum**2 ) / (coeff_dictionary["Ar_40"]))**2
                case "He":
                    if "4" != error_factor_key:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  RAW_dictionary[key]/RAW_sum**2 ) / (coeff_dictionary["He_4"]))**2
                    else:
                        ppm_stdev_dictionary[key] += ((ic_stdev_dictionary[error_factor_key])*(  (RAW_sum - RAW_dictionary[key])/RAW_sum**2 ) / (coeff_dictionary["He_4"]))**2
    
    ppm_stdev_dictionary["N2"] += (ppm_stdev_dictionary["CO2"]*coeff_dictionary["CO2_28"])/coeff_dictionary["CO2_44"]

    for key in ppm_stdev_dictionary:
        ppm_stdev_dictionary[key] = ((ppm_stdev_dictionary[key])**0.5)*1000000


    return ppm_stdev_dictionary

                    



def main(ppm_dictionary):
    RAW_dictionary, ic_dictionary, ic_stdev_dictionary = ConvertPPMtoIC(ppm_dictionary)
    ppm_stdev_dictionary = FindQuadraticError( RAW_dictionary, ppm_dictionary, ic_dictionary, ic_stdev_dictionary, raw_coeff=0.0005 )

    print(ppm_stdev_dictionary)




if __name__== "__main__":
    main(ppm_dictionary={"CO2":1000000, "CH4":0, "O2":0, "N2":0, "Ar":0, "He":0})