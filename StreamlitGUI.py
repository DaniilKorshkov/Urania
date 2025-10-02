import streamlit as st
import pandas as pd
import pickle as pk
import numpy as np
import matplotlib.pyplot as plt
import Functions as fn
import datetime as dt
import JSONoperators as js
import datetime
import streamlit.components.v1 as components
import math
import AbnormalityReaction as ar
import GUI_File_Manager as fm
import matplotlib.ticker as ticker




def append_arrays(array1,array2,i):
    array1.append(i)
    array2.append()

def refresh():
    return True


def date_time_input():  # function to input date and time as seconds from 01jan1970 through graphic user interface


    col = st.columns((1, 1), gap='medium')  # left part of the screen to input date, right - to input time
    with col[0]:
        date_value = st.date_input(label="Enter date: ",min_value=datetime.date(1969,1,1))
    with col[1]:
        time_value = st.time_input(label="Enter time: ")

    date_value = str(date_value) # obtained results converted to strings and then split into integers
    time_value = str(time_value)

    date_array = date_value.split("-")
    time_array = time_value.split(":")

    #print(date_array)
    #print(time_array)

    datetime_value = (datetime.datetime(year=int(date_array[0]),month = int(date_array[1]),day=int(date_array[2]),hour=int(time_array[0]),minute=int(time_array[1]),second=int(time_array[2]))).timestamp()
    return datetime_value  #integers are merged together using datetime.datetime and then returned







def three_dimentional_spectrum(spectrum_list, initial_value, step):  # function to display 3d plot with M and time on x,y axis and PPM on z axis
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    timeframe = fn.get_time_list(spectrum_list)  #list of all moments of time for given spectrum





    for time_moment in timeframe:

        mass_range = list()  # create array for X line with respect to initial mass value and step length
        for i in range(len(spectrum_list[str(time_moment)])):
            mass_range.append(initial_value + i * step)
        ys = spectrum_list[str(time_moment)]



        # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
        ax.bar(mass_range, ys, zs=time_moment, zdir='y', alpha=0.8)

    ax.set_xlabel('M')
    ax.set_ylabel('time')
    ax.set_zlabel('PP(M?)')

    ax.set_title(f"Spectrums for different time moments")

    # On the y-axis let's only label the discrete values that we have data for.
    #ax.set_yticks(yticks)



    st.pyplot(fig)









def constant_time_spectrum(spectrum_list, oxygen_list, custom_names_list, initial_value, step, islogarithmic, isppm):   # function to display spectrum for given moment of time



    #initial_load_time = datetime.datetime.now()
    time_array = fn.get_time_list(spectrum_list)   # get all moments of time from loaded spectrums
    #final_load_time = datetime.datetime.now()
    #print(f"Loading time = {final_load_time-initial_load_time}")


    if len(time_array) == 0:
        st.write(f"File is empty, cannot display constant time mass spectrum")
    else:

        try:
            given_time_tick = st.slider(label="Select time: ",max_value=(len(time_array)-1))  # select moment of time from list of loaded spectrums
        except:
            given_time_tick = 0

        given_time = time_array[given_time_tick]   # get desired moment of time


        placeholder = st.empty()
        with placeholder.container():



            assert spectrum_list[str(given_time)] != None



            fig, ax = plt.subplots()

            mass_range = list()  # create array for X line with respect to initial mass value and step length
            for i in range(len(spectrum_list[str(given_time)])):
                mass_range.append(initial_value+i*step)



            #print(mass_range)
            display_range = spectrum_list[str(given_time)]
            oxygen = oxygen_list[str(given_time)]
            print(oxygen)
            oxygen_label = "Oxygen ppm"
            table_range = display_range
            ylabel = "ATM"

            if isppm == "True":
                    pascal_sum = 0
                    for element in spectrum_list[str(given_time)]:
                        pascal_sum = pascal_sum + element
                    new_range = []
                    for element in display_range:
                        new_range.append((element * 1000000) / pascal_sum)

                    display_range = new_range
                    table_range = display_range
                    ylabel = "PPM"



            if islogarithmic == "True":
                ax.set_yscale('symlog')
                ylabel = f'log10 {ylabel}'
                oxygen_label = "log10 oxygen ppm"
                if isppm == "True":
                    ax.set_ylim([1, 2000000])
                else:
                    ax.set_ylim([1, 1000000000])
            else:
                if isppm == "True":
                    ax.set_ylim([1, 1100000])
                else:
                    ax.set_ylim([1, 500000000])





            ax.bar(mass_range, display_range, label="constant time spectrum",width=0.8*step) #  range(len(spectrum_list[str(given_time)]) is array of molar masses, from 0 to maximal molar mass specified in spectrum



            ax.set_xlabel(f'M')
            ax.set_ylabel(ylabel)
            ax.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
            ax.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

            ax.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
            ax.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)

            try:
                
                custom_line_name = str(custom_names_list[str(given_time)])
                ax.set_title(custom_line_name)

            except:

                ax.set_title(f'Mass spectrum for time: {dt.datetime.fromtimestamp(given_time)}')


            st.pyplot(fig)
            st.write(f"{oxygen_label}: {oxygen}")

        do_display_table = st.button(label="Display table with values")
        if do_display_table:
            yylabel = ylabel.strip("log10")
            st.write(pd.DataFrame({
                'M/Z': mass_range,
                f'{yylabel}': display_range}))














def constant_mass_spectrum(spectrum_list,oxygen_list,solutions_list,default_mass_string, initial_value, step, islogarithmic, isppm, isinterpreted):  # function to display plots for constant masses with time on X axis and PPM on Y axis

    if spectrum_list == None or len(spectrum_list) == 0:
        st.write(f"No data had been recorded yet")


    else:


        
        
        
        if isinterpreted == "False":

            st.write(f"Enter desired M/Z separated by comma: (default: {default_mass_string}) ")
            mass_string = st.text_input(label="Enter desired M/Z (or 'ox') separated by comma: ")
            if mass_string == "":
                mass_string = default_mass_string  # user is promted to input list of desired masses as string. If nothing is inputed, default list is used

            temp_mass_list = (mass_string.strip()).split(",")
            mass_list = []  # list of desired molar masses to be displayed on graph




        
            for element in temp_mass_list:

                if element.strip() == "ox":
                    mass_list.append("ox")
                    #st.write(type(len(spectrum_list[0])))

                else:
                    try:
                        float_mass = float(element.strip())


                        temp_timestamp = list(spectrum_list)[0]
                        if (float_mass < initial_value ) or (float_mass > (initial_value + step*(len(spectrum_list[temp_timestamp]) )-1) ):
                            st.write(f"M/Z {float_mass} is out of limit")




                        else:

                                mass_list.append(float_mass)


                    except:
                        st.write(f"{element.strip()} is not a valid M/Z")

            if len(mass_list) == 0:
                st.write("No valid M/Z provided to display")
            else:







                placeholder = st.empty()
                with placeholder.container():
                    fig, ax = plt.subplots()
                    x = fn.get_time_list(spectrum_list)
                    x_converted = [dt.datetime.fromtimestamp(element) for element in x]  # convert date and time from computer format to human readable format


                    

                    mass_dictionary = {}  # dictionaty to be displayed in table with numerical values
                    mass_dictionary[f"Time:"] = x_converted   # first column is time moments of measurements

                    for given_mass in mass_list:

                        if given_mass == "ox":
                            y = []
                            for key in oxygen_list:
                                print(oxygen_list[key])
                                y.append(oxygen_list[key])


                        else:
                            mass_number = int((given_mass-initial_value)/step)
                            #st.write(mass_number)
                            try:
                                y = fn.plot_mass(spectrum_list, mass_number,isppm)
                            except:
                                pass

                        display_range = y



                        if isppm == "True":
                            ylabel = "PPM"
                        else:
                            ylabel = "ATM"

                        if (islogarithmic == "True" and isppm == "True"):
                            ax.set_yscale('symlog')
                            if isppm == "True":
                            ax.set_ylim([1, 2000000])
                        elif (islogarithmic == "True" and isppm == "False"):
                            ax.set_yscale('symlog')
                            ax.set_ylim([1, 500000000])
                        


                        mass_dictionary[f"M/Z = {str(given_mass)}"] = y


                        ax.plot(x_converted, display_range, label=f"M/Z: {given_mass}")



        if isinterpreted == "True":

                        x = fn.get_time_list(spectrum_list)
                        x_converted = [dt.datetime.fromtimestamp(element) for element in x]

                        mass_dictionary = {}  # dictionaty to be displayed in table with numerical values
                        mass_dictionary[f"Time:"] = x_converted


                        fig, ax = plt.subplots()
                        x = fn.get_time_list(spectrum_list)

                        y_oxygen = []
                        for key in oxygen_list:
                            y_oxygen.append(oxygen_list[key])
                        

                        display_range = y_oxygen
                        ax.plot(x_converted, display_range, label=f"O2 (electrochemical)")
                        mass_dictionary[f"O2 (electrochemical)"] = y_oxygen


                        compounds_of_interest_list = []
                        for time_key in solutions_list:
                            
                            for compound_key in solutions_list[time_key]["interpreted_spectrum"]:
                                compounds_of_interest_list.append(compound_key)
                                
                            
                            break




                        for key in compounds_of_interest_list:
                            y = []
                            for time_key in solutions_list:
                                if isppm == "False":
                                    y.append(  solutions_list[time_key]["interpreted_spectrum"][key])
                                if isppm == "True":
                                    partial_pressures_sum = 0
                                    for compound_key in compounds_of_interest_list:
                                        partial_pressures_sum += abs(solutions_list[time_key]["interpreted_spectrum"][compound_key])
                                    y.append(  (abs(solutions_list[time_key]["interpreted_spectrum"][key])*1000000/partial_pressures_sum ) )


                            display_range = y
                            
                            mass_dictionary[f"{key}"] = y
                            ax.plot(x_converted, display_range, label=f"{key}")



                        if isppm == "True":
                            ylabel = "PPM"
                        else:
                            ylabel = "ATM"

                        if (islogarithmic == "True" and isppm == "True"):
                            ax.set_yscale('symlog')
                            ax.set_ylim([1, 2000000])
                        elif (islogarithmic == "True" and isppm == "False"):
                            ax.set_yscale('symlog')
                            ax.set_ylim([0, 2])
                        


                        


                        






                    







        ax.set_ylabel(ylabel)



        ax.set_xlabel(f'Time')
        ax.set_ylabel(ylabel)

        ax.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
        ax.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

        ax.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
        ax.tick_params('x', labelrotation=90)
        ax.legend()
        if isinterpreted == "False":
            ax.set_title(f'Ionic current {ylabel} vs time for specified M')
        if isinterpreted == "True":
            ax.set_title(f'Concentration of gases vs time')

        #ax.xaxis.axis_date(tz=None)

        st.pyplot(fig)

        do_display_table = st.button(label="display table with values")  # optionally display table with numerical values
        if do_display_table:
            st.write(pd.DataFrame(mass_dictionary))






def display_one_sample_data(settings_filename,self_name):           # function to display all 3 plots for given sample

    


    Settings = js.ReadJSONConfig("manual_inspect_settings","settings")   # settings are imported from JSON config



    spectrum_name = fm.SpectrumsDropdownMenu()
    if spectrum_name == None:

        st.write("No spectrum files found")
    else:

        st.write(f"Reading logs from {str(spectrum_name)} source")
        parsing_mode = st.selectbox("Parsing mode",["last","search"])

        st.write(f"{parsing_mode} mode of operation")

        #time_moment = Settings["default_moment_of_time"]
        if parsing_mode == "search":  #get desired moment of time is parsing mode is search
            #time_moment = st.text_input("Moment of time to search for: ")
            #time_moment = int(date_time_input())


            time_moment = int(date_time_input())



            st.write(f"Time = {dt.datetime.fromtimestamp(time_moment)}")





        howmuchspectrums = TimeInputWidget()





        howmuchspectrums = int(howmuchspectrums) # assert that howmuchspectrums is int and greater than 0
        assert howmuchspectrums > 0

        if parsing_mode == "last":
                metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = js.read_last_spectrums_for_time(spectrum_name, howmuchspectrums)   # most recent spectrums are imported from JSON file
        else:
                metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = js.read_period_of_time_wrt_time(spectrum_name,howmuchspectrums,time_moment)

        if metadata["is_a_spectrum"] != "True":   # verification that provided file is a spectrum
                st.write("Imported file is not valid!")

        initial_value, step = metadata["initial_value"],metadata["step"]








        islogarithmic = st.radio(f"Do display logarithmic scalе?", ["True", "False"])
        isppm = st.radio(f"Do convert to ppm?", ["True", "False"])
        
        constant_time_spectrum(spectrum_list, oxygen_list, custom_names_list, initial_value, step, islogarithmic,isppm)


        islogarithmic2 = st.radio(f"Do display logarithmic scale2?", ["True", "False"])
        isppm2 = st.radio(f"Do convert to ppm2?", ["True", "False"])
        isinterpreted = st.radio(f"Do show interpreted spectra?", ["True", "False"])
        constant_mass_spectrum(spectrum_list,oxygen_list,solutions_list,Settings["default_masses"], initial_value, step, islogarithmic2, isppm2,isinterpreted)

        find_abnormalities = st.button("Find abnormalities")
        if find_abnormalities:

                    if_abnormalities,log_entries_list = ar.AnalyzeInterpretedFile(spectrum_name)
                    if if_abnormalities:
                        for element in log_entries_list:
                            st.write(element)
                    else:
                        st.write("No abnormalities found in this file")



        #except:
            #st.write("Bad input in howmuchspectrums/momentoftime line!!!")

        final_load_time = datetime.datetime.now()
        #print(f"Total time = {final_load_time - initial_load_time}")


def TestGUI():  # test function that is not used

    st.write("Here's our first attempt at using data to create a table:")
    st.write("Here's our first attempt at using data to create a table:")
    st.write("Here's our first attempt at using data to create a table:")
    st.write(pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 50]
    }))

    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)

    st.pyplot(fig)


def TimeInputWidget():
    col = st.columns((1, 1, 1), gap='medium')
    with col[0]:
        days = st.text_input(
            label="How much days of data to display: ")  # user is prompted to override amount of displayed spectrums
    with col[1]:
        hours = st.text_input(
            label="How much hours of data to display: ")  # user is prompted to override amount of displayed spectrums
    with col[2]:
        minutes = st.text_input(
            label="How much minutes of data to display: ")  # user is prompted to override amount of displayed spectrums

    if days == None:   # if not specified, value is set to zero
        days = 0
    if hours == None:
        hours = 0
    if minutes == None:
        minutes = 1


    try:   #if invalid values specified by user, values are set to zero
        days = int(days)
    except:
        days = 0
    try:
        hours = int(hours)
    except:
        hours = 0
    try:
        minutes = int(minutes)
    except:
        minutes = 1



    ret = int( 86400*days + 3600*hours + 60*minutes )
    return ret