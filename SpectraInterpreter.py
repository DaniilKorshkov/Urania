import numpy as np
import JSONoperators as js


def solve_mass_spectrum(mass_spectrum):  # mass spectrum is interpreted as least-square solution of overdefined square equation


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



if __name__ == "__main__":
    print(solve_mass_spectrum( [6196.557152312657, 374.3790482353278, -170.67536628831482, 250.09293282992374, 130.88237011085118, 33.99307584690966, 22.70768180760403, 280.9032196839713, -173.1592511566743, -0.0, 34.07738052783453, 126.00349905007273, -56.72085577671643, 124.51927102032144, 34.185607945564975, 68.18290986895764, 476.587051274673, 2354.8359500115016, 135.80818781737588, 147.16108391707272, 79.2231842169228, 22.69133256681598, -181.43979291511292, -0.0, 67.91721766844107, -22.636885551072496, 113.50650124477357, 850.7194474194567, -169.8735768874239, -351.11531505018456, 91.04600289464861, -45.407586717219424, -102.39437085329091, -45.44090515000064, 7010.880533487443, 495496.6740297175, 1444.6697544147444, 100154.9059508913, 2087798.28463471, 153103585.19136018, 1782.4434105208175, -102.03614078187734, 22.729532902642376, 170.31807003415202, -45.326298023706926, -90.7143198324916, -260.4293916067259, -102.29054319332462, 113.48556427525654, 4.530407284495171] ))
