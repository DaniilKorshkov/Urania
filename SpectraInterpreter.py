import numpy as np
import JSONoperators as js
import json
import subprocess
from ConvertCsvScanToList import read_filename

def solve_mass_spectrum_old(mass_spectrum):  # mass spectrum is interpreted as least-square solution of overdefined square equation


    samples_dict = js.ReadJSONConfig("cracking_patterns","list")
    other_factors_dict = js.ReadJSONConfig("other_factors_patterns","list")

    for key in samples_dict:
        assert len(mass_spectrum) == len(samples_dict[key])
    
    for key in other_factors_dict:
        assert len(mass_spectrum) == len(other_factors_dict[key])

    
    new_mass_spectrum = []
    for element in mass_spectrum:
        new_mass_spectrum.append(abs(element))
    
    mass_spectrum = new_mass_spectrum

    
    similar_entries_found = False
    for key in samples_dict:
        try:
            void = other_factors_dict["key"]
            similar_entries_found = True
        except:
            pass
    
    if similar_entries_found:
        raise Exception("Two equivalent variables names were encountered in samples list and noise factors list")



    left_side_matrix_raw = []
    variables_list_raw = []




    
    for key in samples_dict:
        variables_list_raw.append(key)
        left_side_matrix_raw.append(samples_dict[key])
    
    for key in other_factors_dict:
        variables_list_raw.append(key)
        left_side_matrix_raw.append(other_factors_dict[key])

    
    left_side_matrix = np.array(left_side_matrix_raw)
    left_side_matrix = left_side_matrix.transpose()
    

    print(mass_spectrum)

    solutions_numpy_array = np.linalg.lstsq(left_side_matrix, mass_spectrum)
    samples_solutions_dictionary = {}
    other_factors_solutions_dictionary = {}

    counter = 0
    for key in samples_dict:
        samples_solutions_dictionary[key] = float(solutions_numpy_array[0][counter])
        counter += 1
    for key in other_factors_dict:
        other_factors_solutions_dictionary[key] = float(solutions_numpy_array[0][counter])
        counter += 1

    

    stdev = float((solutions_numpy_array[1])[0])

    return samples_solutions_dictionary, other_factors_solutions_dictionary, stdev



def solve_mass_spectrum(mass_spectrum):  # mass spectrum is interpreted as least-square solution of overdefined square equation


    cracking_patterns = js.ReadJSONConfig("cracking_patterns", "list")

    
    
    new_mass_spectrum = []
    for element in mass_spectrum:
        new_mass_spectrum.append(abs(element))
    
    mass_spectrum = new_mass_spectrum

    
    he_4 = cracking_patterns["He_4"]
    ar_40 = cracking_patterns["Ar_40"]
    co2_44 = cracking_patterns["CO2_44"]
    co2_28 =  cracking_patterns["CO2_28"]
    ch4_15 = cracking_patterns["CH4_15"]
    n2_28 = cracking_patterns["N2_28"]
    o2_32 = cracking_patterns["O2_32"]


    he_ic = new_mass_spectrum[3]/he_4
    ar_ic = new_mass_spectrum[39]/ar_40
    co2_ic = new_mass_spectrum[43]/co2_44
    co2_28_current = co2_ic*co2_28
    ch4_ic = new_mass_spectrum[14]/ch4_15
    o2_ic = new_mass_spectrum[31]/o2_32
    n2_ic = (new_mass_spectrum[27] - co2_28_current)/n2_28



    samples_solutions_dictionary = {"He":he_ic, "Ar":ar_ic, "CO2":co2_ic, "CH4":ch4_ic, "O2":o2_ic, "N2":n2_ic}
    other_factors_solutions_dictionary = {"N2H":new_mass_spectrum[28], "ArH":new_mass_spectrum[40], "H2O":new_mass_spectrum[17]}
    stdev = 0

    return samples_solutions_dictionary, other_factors_solutions_dictionary, stdev


    
''' 
def solve_mass_spectrum_ROOT(mass_spectrum):

    cracking_patterns = js.ReadJSONConfig("cracking_patterns", "list")
    cwd = js.ReadJSONConfig("cwd", "cwd")
    
    he_4 = cracking_patterns["He_4"]
    ar_40 = cracking_patterns["Ar_40"]
    co2_44 = cracking_patterns["CO2_44"]
    co2_28 =  cracking_patterns["CO2_28"]
    ch4_15 = cracking_patterns["CH4_15"]
    n2_28 = cracking_patterns["N2_28"]
    o2_32 = cracking_patterns["O2_32"]

    comma_separated_arguements = [f"{cwd}/spectre_to_ppm_converter","1", "1", str(len(mass_spectrum)),"6"]
    for element in mass_spectrum:
        comma_separated_arguements.append(str(element))

    comma_separated_arguements.append("0")
    comma_separated_arguements.append("4")
    comma_separated_arguements.append(str(he_4))

    comma_separated_arguements.append("1")
    comma_separated_arguements.append("40")
    comma_separated_arguements.append(str(ar_40))

    comma_separated_arguements.append("2")
    comma_separated_arguements.append("32")
    comma_separated_arguements.append(str(o2_32))

    comma_separated_arguements.append("3")
    comma_separated_arguements.append("28")
    comma_separated_arguements.append(str(n2_28))

    comma_separated_arguements.append("4")
    comma_separated_arguements.append("44")
    comma_separated_arguements.append(str(co2_44))

    comma_separated_arguements.append("5")
    comma_separated_arguements.append("15")
    comma_separated_arguements.append(str(ch4_15))


   

    CSV_concentrations = (((subprocess.run(comma_separated_arguements,capture_output=True,cwd=cwd)).stdout).decode("utf-8")).strip("\n")

    print(CSV_concentrations)'''

def solve_mass_spectrum_ROOT(mass_spectrum,initial_mass,step):
    element_lookup_dictionary = {"He":"0","Ar":"1","O2":"2","N2":"3","CO2":"4","CH4":"5"}
    calibration_parameters_dictionary = js.ReadJSONConfig("cracking_patterns", "list")
    cwd = js.ReadJSONConfig("cwd", "cwd")
    
    

    comma_separated_arguements = [f"{cwd}/spectre_to_ppm_converter",str(initial_mass), str(step), str(len(mass_spectrum)),str(len(calibration_parameters_dictionary))]
    for element in mass_spectrum:
        comma_separated_arguements.append(str(element))

    
    for key in calibration_parameters_dictionary:
        split_key = key.split("_")

        comma_separated_arguements.append( element_lookup_dictionary[split_key[0]] )
        comma_separated_arguements.append( split_key[1] )
        comma_separated_arguements.append( str(calibration_parameters_dictionary[key]) )
         
         


   
    print(comma_separated_arguements)
    CSV_concentrations = (((subprocess.run(comma_separated_arguements,capture_output=True,cwd=cwd)).stdout).decode("utf-8")).strip("\n")

    print(CSV_concentrations)







def calibrate_rga_ROOT(mass_spectrum_array,initial_mass,step):
    element_lookup_dictionary = {"He":"0","Ar":"1","O2":"2","N2":"3","CO2":"4","CH4":"5"}
    cwd = js.ReadJSONConfig("cwd", "cwd")

    calibration_parameters_dictionary = js.ReadJSONConfig("cracking_patterns", "list")


    comma_separated_arguements = [f"{cwd}/calibration_calculator",str(initial_mass), str(step),  str(len((mass_spectrum_array[0])["scan"])), str(len(mass_spectrum_array)), str(len(calibration_parameters_dictionary))]


    for element in mass_spectrum_array:
        for subelement in element["scan"]:
            comma_separated_arguements.append(str(subelement))
    
    for element in mass_spectrum_array:
        for subelement in element["ppm"]:
            comma_separated_arguements.append(str(subelement))


    calibration_parameter_indexation_list = []
    for key in calibration_parameters_dictionary:
        split_key = key.split("_")

        comma_separated_arguements.append( element_lookup_dictionary[split_key[0]] )
        comma_separated_arguements.append( split_key[1] )
         
        calibration_parameter_indexation_list.append(key)       
        
                
             
    


    

    raw_output = (((subprocess.run(comma_separated_arguements,capture_output=True,cwd=cwd)).stdout).decode("utf-8")).strip("\n")
    

    split_raw_output = raw_output.split(" ")
    calibration_parameter_list = split_raw_output[(len(split_raw_output) - len(calibration_parameters_dictionary) - 1 ):len(split_raw_output)]
    


    new_calibration_dictionary = {}
    for i in range(len(calibration_parameter_indexation_list)):
        new_calibration_dictionary[calibration_parameter_indexation_list[i]] = float((calibration_parameter_list[i]).strip("(limited)\n"))
    
    for key in new_calibration_dictionary:
        print(f"{key}: {new_calibration_dictionary[key]}")

    
    old_config_line = js.ReadJSONConfig("cracking_patterns")
    old_config_line["list"] = new_calibration_dictionary
    js.EditJSONConfig("cracking_patterns",json.dumps(old_config_line))





def calibrate_rga_ROOT_2(mass_spectrum):
    cwd = js.ReadJSONConfig("cwd", "cwd")
    comma_separated_arguements = [f"{cwd}/calibration_calculator","1", "1",  str(len(mass_spectrum)),"1","6"]

    for element in mass_spectrum:
        comma_separated_arguements.append(str(element))

    

    ppm_array = ["10000","10000","10000","10000","960000","10000"]

    for element in ppm_array:
        comma_separated_arguements.append(str(element))

    


    parameter_definitions = ["0","4","1","40","2","32","3","28","4","44","5","15"]

    for element in parameter_definitions:
        comma_separated_arguements.append(str(element))

    CSV_concentrations = (((subprocess.run(comma_separated_arguements,capture_output=True,cwd=cwd)).stdout).decode("utf-8")).strip("\n")

    print(CSV_concentrations)






#CSV_concentrations = subprocess.run(["input_test",comma-separated-arguements],capture_output=True,cwd=cwd)


if __name__ == "__main__":
    
    #calibrate_rga_ROOT_2([2507.628127884217, 283.32912811106195, 500.41344493032625, 3143.632926217696, -65.34057504680752, -260.9866511678882, 65.37488054401338, 370.43081772279197, 217.31368153111038, -130.51395864276745, 935.3849758320902, 644920.8717542005, 34436.05309367704, 109883.36932276537, 645297.5928678942, 6504943.388273818, 13229.290047016202, 23036.82831012785, 435.89095216260955, 217.5605550959866, 130.7784699289605, -217.56818619099357, 130.68288092730225, 239.2813812889088, -326.28058790831824, 108.97273804065223, 55228.10642735145, 6876444.17059916, 70925.51509507086, 12038.42118480004, 3851.0080071153316, 416075.2456707255, 435.06756711581795, 1674.929214665803, 43.57263546856219, 2785.1113369233303, 65.26816259060656, 632.0114034187445, 11289.879886353376, 962244.7935221458, 174.33723648680467, 2241.0655224152943, 533628.4526805484, 69806776.54876031, 806619.1333779099, 277370.8142221149, 3156.849020773373, 217.58443194205617, -195.88579599016168, -3.6227832250226837])

    initial_mass = 1
    step = 1
    amount_of_steps = 50
    

    
    files_for_calibration = [{"filename":"cgas-em-000067.csv","ppm":["0","100","0","999900","0","0"]},
    {"filename":"cgas-fc-000001.csv","ppm":["0","1000000","0","0","0","0"]},
    {"filename":"cgas-fc-000001.csv","ppm":["0","1000000","0","0","0","0"]},
    {"filename":"cgas-em-000021.csv","ppm":["0","100","0","0","100000","0"]},
    {"filename":"cgas-em-000021.csv","ppm":["0","100","0","0","100000","0"]},
    {"filename":"cgas-em-000021.csv","ppm":["0","100","0","0","100000","0"]},
    {"filename":"cgas-em-000021.csv","ppm":["0","100","0","0","100000","0"]}]
    


    calibration_input_parameters = []

    for file in files_for_calibration:
        
        rga_scan = read_filename(file["filename"],initial_mass,step,amount_of_steps)
        
        calibration_input_parameters.append({"scan":rga_scan, "ppm":(file["ppm"])})
    
    
    calibrate_rga_ROOT(calibration_input_parameters,initial_mass,step)


    #calibrate_rga_ROOT([{"scan":[2507.628127884217, 283.32912811106195, 500.41344493032625, 31430.632926217696, -65.34057504680752, -260.9866511678882, 65.37488054401338, 370.43081772279197, 217.31368153111038, -130.51395864276745, 935.3849758320902, 644920.8717542005, 34436.05309367704, 109883.36932276537, 645297.5928678942, 6504943.388273818, 13229.290047016202, 23036.82831012785, 435.89095216260955, 217.5605550959866, 130.7784699289605, -217.56818619099357, 130.68288092730225, 239.2813812889088, -326.28058790831824, 108.97273804065223, 55228.10642735145, 6876444.17059916, 70925.51509507086, 12038.42118480004, 3851.0080071153316, 416075.2456707255, 435.06756711581795, 1674.929214665803, 43.57263546856219, 2785.1113369233303, 65.26816259060656, 632.0114034187445, 11289.879886353376, 962244.7935221458, 174.33723648680467, 2241.0655224152943, 533628.4526805484, 69806776.54876031, 806619.1333779099, 277370.8142221149, 3156.849020773373, 217.58443194205617, -195.88579599016168, -3.6227832250226837],"ppm":["10000","10000","10000","10000","960000","10000"]},{"scan":[2507.628127884217, 283.32912811106195, 500.41344493032625, 31430.632926217696, -65.34057504680752, -260.9866511678882, 65.37488054401338, 370.43081772279197, 217.31368153111038, -130.51395864276745, 935.3849758320902, 644920.8717542005, 34436.05309367704, 109883.36932276537, 645297.5928678942, 6504943.388273818, 13229.290047016202, 23036.82831012785, 435.89095216260955, 217.5605550959866, 130.7784699289605, -217.56818619099357, 130.68288092730225, 239.2813812889088, -326.28058790831824, 108.97273804065223, 55228.10642735145, 6876444.17059916, 70925.51509507086, 12038.42118480004, 3851.0080071153316, 416075.2456707255, 435.06756711581795, 1674.929214665803, 43.57263546856219, 2785.1113369233303, 65.26816259060656, 632.0114034187445, 11289.879886353376, 962244.7935221458, 174.33723648680467, 2241.0655224152943, 533628.4526805484, 69806776.54876031, 806619.1333779099, 277370.8142221149, 3156.849020773373, 217.58443194205617, -195.88579599016168, -3.6227832250226837],"ppm":["10000","10000","10000","10000","960000","10000"]}],1,1)
    #solve_mass_spectrum_ROOT([2507.628127884217, 283.32912811106195, 500.41344493032625, 31430.632926217696, -65.34057504680752, -260.9866511678882, 65.37488054401338, 370.43081772279197, 217.31368153111038, -130.51395864276745, 935.3849758320902, 644920.8717542005, 34436.05309367704, 109883.36932276537, 645297.5928678942, 6504943.388273818, 13229.290047016202, 23036.82831012785, 435.89095216260955, 217.5605550959866, 130.7784699289605, -217.56818619099357, 130.68288092730225, 239.2813812889088, -326.28058790831824, 108.97273804065223, 55228.10642735145, 6876444.17059916, 70925.51509507086, 12038.42118480004, 3851.0080071153316, 416075.2456707255, 435.06756711581795, 1674.929214665803, 43.57263546856219, 2785.1113369233303, 65.26816259060656, 632.0114034187445, 11289.879886353376, 962244.7935221458, 174.33723648680467, 2241.0655224152943, 533628.4526805484, 69806776.54876031, 806619.1333779099, 277370.8142221149, 3156.849020773373, 217.58443194205617, -195.88579599016168, -3.6227832250226837],1,1)
