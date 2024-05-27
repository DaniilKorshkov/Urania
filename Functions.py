def get_time_list(spectrum_list): # get all moments of time from given array of spectrums
    time_list = []
    for time_moment in spectrum_list:
        time_list.append(float(time_moment))
    return(time_list)


'''def incriment_time(current_time_tick, time_list):
    current_time_tick = (current_time_tick+1)%len(time_list)
    return current_time_tick, time_list[current_time_tick]

def decriment_time(current_time_tick, time_list):
    current_time_tick = (current_time_tick-1)%len(time_list)
    return current_time_tick, time_list[current_time_tick]'''

def plot_mass(spectrum_list, given_mass):  # parse through array of spectrums to get list of PPM's for given mass over amount of time
    mass_plot = []
    for time_key in spectrum_list:
        mass_plot.append( (spectrum_list[time_key])[given_mass] )
    return mass_plot


#print(incriment_time(3,[1,2,3,4]))