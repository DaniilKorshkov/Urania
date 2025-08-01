import numpy as np
import JSONoperators as js


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


    
   



if __name__ == "__main__":
    print(solve_mass_spectrum( [2507.628127884217, 283.32912811106195, 500.41344493032625, 31436.32926217696, -65.34057504680752, -260.9866511678882, 65.37488054401338, 370.43081772279197, 217.31368153111038, -130.51395864276745, 935.3849758320902, 644920.8717542005, 34436.05309367704, 109883.36932276537, 645297.5928678942, 6504943.388273818, 13229.290047016202, 23036.82831012785, 435.89095216260955, 217.5605550959866, 130.7784699289605, -217.56818619099357, 130.68288092730225, 239.2813812889088, -326.28058790831824, 108.97273804065223, 55228.10642735145, 6876444.17059916, 70925.51509507086, 12038.42118480004, 3851.0080071153316, 416075.2456707255, 435.06756711581795, 1674.929214665803, 43.57263546856219, 2785.1113369233303, 65.26816259060656, 632.0114034187445, 11289.879886353376, 962244.7935221458, 174.33723648680467, 2241.0655224152943, 533628.4526805484, 69806776.54876031, 806619.1333779099, 277370.8142221149, 3156.849020773373, 217.58443194205617, -195.88579599016168, -3.6227832250226837] ))
    print(solve_mass_spectrum( [6260.0592276112875, 101324.97519391228, 503.38413524988255, 17640.900862184826, -7.202864736515226, -50.32912021865966, -93.46386392753428, -0.0, 7.201726218160466, -0.0, -100.64940521449435, 36.0054671445847, -115.23470031224443, 14298.587884630906, 143.7836063422626, 17477.743022959326, 2881.1078602657994, 16275.61732435214, 93.4511382739095, 179.71135660562763, -57.50914791059329, -0.0, 21.609922121117666, -93.45360205476759, 43.21187090960241, -100.65072869350298, 3227.460260889512, 482230.090727649, 5934.143860844093, 79.07125683110476, 2631.332378159403, 329497.63839799666, 567.9576920178006, 1395.0195675626367, 2416.37424627739, 273241.58513492387, 1534.4933266119215, 56193.34996084564, 832242.619633785, 88946424.2919683, 289367.0008783351, -7.208592616575606, -14.379939794873087, 273.69924758624614, 107.84431935454244, 71.8899077221255, -50.421823006166846, -50.333320227051445, 57.52657943472096, -2.6344278188963086] )  )
    print(solve_mass_spectrum( [2505.907722492217, 310.6559011965439, 351.013333637072, 20738.29668465525, 89.75585817555172, 8.175478644407885, -114.220678515223, -0.0, 16.315664764086993, 16.320825118855893, 1376.670888849485, 615201.7142107274, 28824.289646008096, 82298.7840942848, 536929.3158431652, 5925822.169609422, 10060.47792959793, 12627.304548117676, 73.17551920490128, 24.455874726123984, 203.84640495140923, 16.288387156714244, 162.89173617946724, -48.77767551602168, 56.898291395995365, 48.78431613037354, 42895.82025183342, 6195724.933530793, 64965.46260688281, 11367.295659961183, 2739.2824107314095, 354997.4378602115, 366.5740250226968, 1650.615791428902, -56.92403748778402, 2902.5143781955603, 170.79912373275928, 577.5347092830284, 10490.445304996209, 1029416.5969972184, 114.12340701582049, 1912.1124217110525, 497779.6506339271, 71035060.66662359, 865121.4360575363, 295192.9924255571, 3424.0708316646133, 366.6641933877356, 40.64663854294579, 0.0] )  )
    print(solve_mass_spectrum( [6571.2594707961325, 100026.61091210527, 625.8341650591195, 17732.680809108842, -109.34903979633177, -101.85760805579743, 87.46309870408895, -36.4581694571111, 145.90763497677838, 50.92947476308653, -7.2753842880442505, 72.75288365709305, 50.933723162915534, 14422.144150239928, 174.59156980163493, 17857.30263709398, 3250.7121342213404, 17482.516440168696, 43.65326059534182, 50.92947476308653, 29.100768665536357, -0.0, 43.65805202372656, -0.0, -7.274585427977471, 29.126342126541108, 3382.694199116491, 480138.0950866245, 5812.8782517662, 36.46665529362494, 2609.8891822720325, 329534.1062046477, 451.1946971598815, 1479.8571682868123, 2516.9732770375, 274392.5720447438, 1433.1939711713892, 56446.3885080642, 866869.0423482559, 89596659.40726906, 280346.4584589653, -43.63562522412328, -0.0, 305.5285592432971, -116.31518062512167, 7.25117282485025, -181.56695121737417, 65.34028415997437, -43.62125390222987, -4.346948018872144 ]))