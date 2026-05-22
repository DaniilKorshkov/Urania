import subprocess
from scipy.special import erfinv
from statistics import stdev
from statistics import mean
from random import random
from sys import stdout


def single_round():

    single_output_dataset = []
    return single_output_dataset



def modify_arguments(arguments,arguments_stdev):

    modified_arguments = []

    for i in range(len(arguments)):
        if (arguments_stdev[i] == 0) or (arguments_stdev[i] == None) or (type(arguments_stdev[i]) != int and type(arguments_stdev[i]) != float) or (type(arguments[i]) != int and type(arguments[i]) != float ):
            modified_arguments.append( str (arguments[i]) )
        else:
            while True:
                randomnumber = 2*random() - 1 
                if (randomnumber < 0.9999999999) and (randomnumber > -0.9999999999):
                    break
                else:
                    pass
            
            stdev_quantity = float(erfinv(randomnumber))
            
            

            modified_arguments.append( str( arguments[i] + 1.41421356237*stdev_quantity*arguments_stdev[i] ) )


    assert ( len(modified_arguments) == len(arguments) )
    return modified_arguments



def main(command,arguments,arguments_stdev,cwd,amount_of_rounds=50000):

    assert( len(arguments) == len(arguments_stdev) )

    output_matrix = []

    percents_finished = 0
    finished_counter_step = 100 / amount_of_rounds



    modified_arguments = modify_arguments(arguments,[0]*len(arguments))
    arguments_list = [command] + modified_arguments
    most_probable_output =  (((subprocess.run(arguments_list,capture_output=True,cwd=cwd)).stdout).decode("utf-8")).strip("\n")
    most_probable_output_array = most_probable_output.split(" ")





    for i in range(amount_of_rounds):

        modified_arguments = modify_arguments(arguments,arguments_stdev)

       
        
        arguments_list = [command] + modified_arguments
        

        single_execution_output = (((subprocess.run(arguments_list,capture_output=True,cwd=cwd)).stdout).decode("utf-8")).strip("\n")
        
        
        single_execution_output_array = single_execution_output.split(" ")

        
        
        output_matrix.append(single_execution_output_array)


        percents_finished += finished_counter_step
        
        #print(f"{percents_finished} % finished ",end="\r")

        stdout.flush()
        stdout.write(f"\r{percents_finished} % finished ")



    output_stdev_array = []
    mean_minus_mp_array = []
    for i in range(len(output_matrix[0])):

        

        try:
            
            placeholder =  float ((output_matrix[0])[i])
            
        except:       
            output_stdev_array.append(0)
            continue

        single_output_dataset = []
        for j in range( amount_of_rounds ):
            single_output_dataset.append( ( float ((output_matrix[j])[i])) )
        
            
        output_stdev_array.append( stdev(single_output_dataset) )
        mean_minus_mp_array.append( mean(single_output_dataset) - float(most_probable_output_array[i]) )
    

    return output_stdev_array, mean_minus_mp_array


if __name__ == "__main__":
    array_to_print, mean_array = main("/home/daniil/Urania/sum_computer",[5,5],[1,1],"/home/daniil/Urania",amount_of_rounds=25000)
    print(array_to_print)
    print(mean_array)
