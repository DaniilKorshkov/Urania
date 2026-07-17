def read_filename(filename, initial_mass, step, amount_of_steps):
    ret = []
    step_counter = 0
    with open(filename,"r") as handle:
        for line in handle:
            linesplit = line.split(",")
            if float(linesplit[0]) == initial_mass + (step*step_counter):

                avg_value = 0
                for i in range( len(linesplit) - 1 ):

                    
                    avg_value += float(linesplit[i+1]) / (len(linesplit) - 1)

                    

                ret.append(avg_value)
                step_counter += 1
            if step_counter == amount_of_steps:
                break

    return ret


if __name__ == "__main__":
    print(read_filename("cgas-em-000067.csv",1,1,50))