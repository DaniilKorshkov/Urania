import numpy as np


def solve_mass_spectrum(mass_spectrum, samples_dict, other_factors_dict):  # mass spectrum is interpreted as least-square solution of overdefined square equation


    for key in samples_dict:
        assert len(mass_spectrum) == len(samples_dict["key"])
    
    for key in other_factors_dict:
        assert len(mass_spectrum) == len(other_factors_dict["key"])


    
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
    

    

    solutions_numpy_array = np.linalg.lstsq(left_side_matrix, mass_spectrum)
    samples_solutions_dictionary = {}
    other_factors_solutions_dictionary = {}

    counter = 0
    for key in samples_dict:
        solutions_dictionary[key] = float(solutions_numpy_array[0][counter])
        counter += 1
    for key in other_factors_dict:
        other_factors_solutions_dictionary[key] = float(solutions_numpy_array[0][counter])
        counter += 1

    

    stdev = float((solutions_numpy_array[1])[0])

    return solutions_dictionary, other_factors_solutions_dictionary, stdev



if __name__ == "__main__":
    print(solve_mass_spectrum( [0,1,2,3,0],  {"ch4":[0,1,0,0,0],"he":[0,0,3,0,0]}  ))
