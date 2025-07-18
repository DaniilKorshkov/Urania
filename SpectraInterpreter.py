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
    print(solve_mass_spectrum( [7199.505549301109, 344.2356598302034, -147.52046200082356, -98.35044465729727, -19.672507999344184, 98.50995560889432, 19.675878123870465, 49.17522232864864, -88.67416116927173, 127.88534584778618, -118.04644593911044, 118.23686683213528, -108.31621881537109, 98.60042196195208, 206.9872485351303, 246.61476089820957, 532.9429430491223, 2977.5861260786533, 89.01674500984761, 49.4350693911702, 217.10390432869266, 118.6009223128769, -167.85793107274557, -167.71055040521307, 69.10946808982975, -9.88171762918013, -118.45464117605783, 375.11134472785756, -78.97843988545807, 39.484365250122245, -29.618084324025627, 59.23460833085754, -39.570294067530206, 49.45439842429419, 4808.804939288974, 528155.6896344635, 1184.9522479391844, 105495.36234811116, 1546515.7383719804, 163462273.24852178, 1629.1090631087213, -9.891139937186828, -109.10686094046964, 49.465907134317455, 188.10589517225523, -0.0, 79.18509192870788, -69.21426080435933, 19.75788180246441, 2.2998109893804783] ))
