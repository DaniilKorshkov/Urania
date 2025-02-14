def get_time_list(spectrum_list): # get all moments of time from given array of spectrums
    time_list = []
    for time_moment in spectrum_list:
        time_list.append(int(time_moment))
    return(time_list)


'''def incriment_time(current_time_tick, time_list):
    current_time_tick = (current_time_tick+1)%len(time_list)
    return current_time_tick, time_list[current_time_tick]

def decriment_time(current_time_tick, time_list):
    current_time_tick = (current_time_tick-1)%len(time_list)
    return current_time_tick, time_list[current_time_tick]'''

def plot_mass(spectrum_list, given_index,isppm):  # look through array of spectrums to get list of PPM's for given mass over amount of time
    mass_plot = []
    for time_key in spectrum_list:
        if isppm == "True":
            pascal_sum = 0
            for element in spectrum_list[time_key]:
                pascal_sum = pascal_sum + abs(element)
            new_range = []
            for element in spectrum_list[time_key]:
                new_range.append((element * 1000000) / pascal_sum)
        else:
            new_range = spectrum_list[time_key]

        mass_plot.append( (new_range)[given_index] )
    return mass_plot


#print(incriment_time(3,[1,2,3,4]))