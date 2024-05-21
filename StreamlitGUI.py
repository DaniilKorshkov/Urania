import streamlit as st
import pandas as pd
import pickle as pk
import numpy as np
import matplotlib.pyplot as plt
import Functions as fn
import datetime as dt
import JSONoperators as js
import datetime
#from datetime import timestamp
import mpld3
import streamlit.components.v1 as components


import schedule
#import Watchdog as wd


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







def three_dimentional_spectrum(spectrum_list):  # function to display 3d plot with M and time on x,y axis and PPM on z axis
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    timeframe = fn.get_time_list(spectrum_list)  #list of all moments of time for given spectrum

    #colors = ['r', 'g', 'b', 'y']
    yticks = [3, 2, 1, 0]
    for time_moment in timeframe:

        xs = np.arange(len(spectrum_list[str(time_moment)]))
        ys = spectrum_list[str(time_moment)]



        # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
        ax.bar(xs, ys, zs=time_moment, zdir='y', alpha=0.8)

    ax.set_xlabel('M')
    ax.set_ylabel('time')
    ax.set_zlabel('PP(M?)')

    ax.set_title(f"Spectrums for different time moments")

    # On the y-axis let's only label the discrete values that we have data for.
    ax.set_yticks(yticks)



    st.pyplot(fig)



def constant_time_spectrum_table(mass_array,ppm_array):
    st.write(pd.DataFrame({
        'Molar mass': mass_array,
        'PPM': ppm_array}))







def constant_time_spectrum(spectrum_list, given_time_tick):   # function to display spectrum for given moment of time

    time_array = fn.get_time_list(spectrum_list)



    try:
        given_time_tick = st.slider(label="Select time: ",max_value=(len(time_array)-1))
    except:
        given_time_tick = 0

    given_time = time_array[given_time_tick]

    placeholder = st.empty()
    with placeholder.container():



        assert spectrum_list[str(given_time)] != None

        fig, ax = plt.subplots()

        ax.bar(range(len(spectrum_list[str(given_time)])), spectrum_list[str(given_time)], label="constant time spectrum") #  range(len(spectrum_list[str(given_time)]) is array of molar masses, from 0 to maximal molar mass specified in spectrum

        ax.set_xlabel(f'M')
        ax.set_ylabel(f'PP(M?)')
        ax.set_title(f'Spectrum for time: {dt.datetime.fromtimestamp(given_time)}')

        st.pyplot(fig)

    do_display_table = st.button(label="Display table with values")
    if do_display_table:
        constant_time_spectrum_table(range(len(spectrum_list[str(given_time)])), spectrum_list[str(given_time)])














def constant_mass_spectrum(spectrum_list,default_mass_string):  # function to display plots for constant masses with time on X axis and PPM on Y axis


    st.write(f"Enter desired molar masses separated by comma: (default: {default_mass_string}) ")
    mass_string = st.text_input(label="Enter desired molar masses separated by comma: ")
    if mass_string == "":
        mass_string = default_mass_string  # user is promted to input list of desired masses as string. If nothing is inputed, default list is used

    try:
        temp_mass_list = (mass_string.strip()).split(",")
        mass_list=[]  # list of desired molar masses to be displayed on graph
        for element in temp_mass_list:
            mass_list.append(int(element.strip()))   #elements from string are splitted, stripped and converted to integers; and appended to mass_list. If not convertable to integers, "bad input" message is printed


        placeholder = st.empty()
        with placeholder.container():
            fig, ax = plt.subplots()
            x = fn.get_time_list(spectrum_list)

            mass_dictionary = {}  # dictionaty to be displayed in table with numerical values
            mass_dictionary[f"Time:"] = x   # first column is time moments of measurements

            for given_mass in mass_list:
                y = fn.plot_mass(spectrum_list, given_mass)
                ax.plot(x, y, label=f"M: {given_mass}",)
                mass_dictionary[f"M = {str(given_mass)}"] = y

            ax.set_xlabel(f'Time')
            ax.set_ylabel(f'PP(M?)')
            ax.legend()
            ax.set_title(f'PPM vs time for given M')

            st.pyplot(fig)

            do_display_table = st.button(label="display table with values")
            if do_display_table:
                st.write(pd.DataFrame(mass_dictionary))


    except:
        st.write("Bad input in mass selection line!!!")



def display_one_sample_data(settings_filename,self_name):           # function to display all 3 plots for given sample

    Settings = js.read_GUI_page_settings(settings_filename,self_name)   # settings are imported from JSON config

    spectrum_name = Settings["spectrum_filename"]
    st.write(f"Reading logs from {str(spectrum_name)} source")
    parsing_mode = Settings["parsing_mode"]
    st.write(f"{parsing_mode} mode of operation")

    time_moment = Settings["default_moment_of_time"]
    if Settings["parsing_mode"] == "search":  #get desired moment of time is parsing mode is search
        #time_moment = st.text_input("Moment of time to search for: ")
        #time_moment = int(date_time_input())

        select_mode = st.selectbox(label="Select how to get time input: ",options=("Current","Default","Select"))

        match select_mode:
            case "Current":
                time_moment = int((datetime.datetime.now()).timestamp())
            case "Default":
                time_moment = int(Settings["default_moment_of_time"])  # by default, time_mode is converted to default in settings
            case "Select":
                time_moment = int(date_time_input())



        st.write(f"Time = {dt.datetime.fromtimestamp(time_moment)}")





    howmuchspectrums = st.text_input(label="How much spectrums to display: ")  # user is prompted to override amount of displayed spectrums
    if howmuchspectrums == "":
        howmuchspectrums = Settings["default_amount_of_spectrums"]  # if not overrided, value is set to default



    try:

        howmuchspectrums = int(howmuchspectrums) # assert that howmuchspectrums is int and greater than 0
        assert howmuchspectrums > 0

        if Settings["parsing_mode"] == "last":
            metadata, spectrum_list = js.read_last_spectrums(Settings["spectrum_filename"], howmuchspectrums)   # most recent spectrums are imported from JSON file
        if Settings["parsing_mode"] == "search":
            metadata, spectrum_list = js.read_period_of_time(Settings["spectrum_filename"],howmuchspectrums,time_moment)

        if metadata["is_a_spectrum"] != "True":   # verification that provided file is a spectrum
            st.write("Imported file is not valid!")



        if Settings["orientation"] == "horizontal":

            #st.set_page_config(layout="wide")
            col = st.columns((1, 1, 1), gap='medium')

            if Settings["do_display_3d"] == "True":
                with col[0]:
                    three_dimentional_spectrum(spectrum_list)
            if Settings["do_display_const_time"] == "True":
                with col[1]:
                    constant_time_spectrum(spectrum_list, 1)
            if Settings["do_display_const_mass"] == "True":
                with col[2]:
                    constant_mass_spectrum(spectrum_list,Settings["default_masses"])

        else:
            if Settings["do_display_3d"] == "True":
                three_dimentional_spectrum(spectrum_list)

            if Settings["do_display_const_time"] == "True":
                constant_time_spectrum(spectrum_list, 1)

            if Settings["do_display_const_mass"] == "True":
                constant_mass_spectrum(spectrum_list,Settings["default_masses"])



    except:
        st.write("Bad input in howmuchspectrums/momentoftime line!!!")













#def spectrum_dashboard(metadata, spectrum_list):
 #   st.write(f"Valve #{metadata["valve_number"]}")



def GUI():  # test function that is not used

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