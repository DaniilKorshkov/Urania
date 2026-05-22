import subprocess
from scipy.special import erfinv
from statistics import stdev
from random import random





def single_round():

    single_output_dataset = []
    return single_output_dataset



def modify_arguments(arguments,arguments_stdev):

    modified_arguments = []

    for i in range(len(arguments)):
        if (arguments_stdev[i] == 0) or (arguments_stdev[i] == None) or (type(arguments_stdev[i]) != int and type(arguments_stdev[i]) != float) or (type(arguments[i]) != int and type(arguments[i]) != float ):
            modified_arguments.append( arguments[i] )
        else:
            while True:
                randomnumber = 2*random() - 1 
                if (randomnumber < 0.9999999999) and (randomnumber > -0.9999999999):
                    break
                else:
                    pass
            
            stdev_quantity = float(erfinv(randomnumber))
            
            

            modified_arguments.append( arguments[i] + stdev_quantity*arguments_stdev[i] )


    assert ( len(modified_arguments) == len(arguments) )
    return modified_arguments



def main(command,arguments,arguments_stdev,cwd,amount_of_rounds=50000):

    assert( len[arguments] == len[arguments_stdev] )

    output_matrix = []

    for i in range(amount_of_rounds):

        modified_arguments = modify_arguments(arguments,arguments_stdev):

        

        single_execution_output = subprocess.run([( [command].append(modified_arguments) ),comma-separated-arguements],capture_output=True,cwd=cwd)

        single_execution_output_array = single_execution_output.split(" ")
        
        output_matrix.append(single_execution_output_array)



    
    for i in range(len(output_matrix[0])):

        output_stdev_array = []

        try:
            placeholder =  float(output_matrix[j])[i]
        except:       
            output_stdev_array.append(0)
            continue

        single_output_dataset = []
        for j in range( amount_of_rounds ):
            single_output_dataset.append( ( float(output_matrix[j])[i]) )
            
        output_stdev_array.append( stdev(single_output_dataset) )
    

    return output_stdev_array


if __name__ == "__main__":
    main()
