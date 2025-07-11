import numpy as np


def solve_mass_spectrum(mass_spectrum, samples_dict):


    for key in samples_dict:
        assert len(mass_spectrum) == len(samples_dict["key"])



    left_side_matrix_raw = []
    variables_list_raw = []




    
    for key in samples_dict:
        variables_list_raw.append(key)
        left_side_matrix_raw.append(samples_dict[key])

    
    left_side_matrix = np.array(left_side_matrix_raw)
    left_side_matrix = left_side_matrix.transpose()
    

    

    solutions_numpy_array = np.linalg.lstsq(left_side_matrix, mass_spectrum)
    solutions_dictionary = {}

    counter = 0
    for key in samples_dict:
        solutions_dictionary[key] = float(solutions_numpy_array[0][counter])
        counter += 1

    

    stdev = float((solutions_numpy_array[1])[0])

    return solutions_dictionary, stdev



if __name__ == "__main__":
    print(solve_mass_spectrum( [0,1,2,3,0],  {"ch4":[0,1,0,0,0],"he":[0,0,3,0,0]}  ))
