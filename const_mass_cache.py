import StreamlitGUI as sg
import JSONoperators as js
import streamlit as st
import datetime as dt
from StreamlitGUI import date_time_input
import math
import pandas as pd
import pickle as pk
import numpy as np
import matplotlib.pyplot as plt
import Functions as fn
import datetime as dt
import JSONoperators as js
import streamlit.components.v1 as components
import math
import AbnormalityReaction as ar
import GUI_File_Manager as fm


def const_mass_cache():
    filelist = js.ReadJSONConfig("cache","current_spectrum_files")

    default_mass_string = js.ReadJSONConfig("cache","default_mass_string")

    st.write(f"Enter desired molar masses separated by comma: (default: {default_mass_string}) ")
    mass_string = st.text_input(label="Enter desired molar masses (or 'ox') separated by comma: ")
    islogarithmic = st.radio(f"Do display logarithmic scalе?", ["True", "False"])
    isppm = st.radio(f"Do convert to ppm?", ["True", "False"])
    if mass_string == "":
        mass_string = default_mass_string  # user is promted to input list of desired masses as string. If nothing is inputed, default list is used


    temp_mass_list = (mass_string.strip()).split(",")
    mass_list=[]  # list of desired molar masses to be displayed on graph
    for element in temp_mass_list:

        if element.strip() == "ox":
            mass_list.append("ox")

        else:
            mass_list.append(float(element.strip()))

    howmuchspectrums = st.text_input(
        label="How much spectrums to display: ")  # user is prompted to override amount of displayed spectrums
    if howmuchspectrums == "":
        howmuchspectrums = 999  # if not overrided, value is set to default

    howmuchspectrums = int(howmuchspectrums)  # assert that howmuchspectrums is int and greater than 0


    assert howmuchspectrums > 0


    parsing_mode = st.selectbox("Parsing mode", ["last", "search"])

    st.write(f"{parsing_mode} mode of operation")


    if parsing_mode == "search":  # get desired moment of time is parsing mode is search
        # time_moment = st.text_input("Moment of time to search for: ")
        # time_moment = int(date_time_input())

        select_mode = st.selectbox(label="Select how to get time input: ", options=("Current", "Default", "Select"))

        match select_mode:
            case "Current":
                time_moment = int((dt.datetime.now()).timestamp())

            case "Select":
                time_moment = int(date_time_input())

        st.write(f"Time = {dt.datetime.fromtimestamp(time_moment)}")






    for spectrum_name in filelist:



        st.write(f"Reading logs from {str(spectrum_name)} source")


        #time_moment = Settings["default_moment_of_time"]


        try:

            if parsing_mode == "last":
                metadata, spectrum_list, oxygen_list = js.read_last_spectrums(spectrum_name,
                                                                              howmuchspectrums)  # most recent spectrums are imported from JSON file
            else:
                metadata, spectrum_list, oxygen_list = js.read_period_of_time(spectrum_name, howmuchspectrums, time_moment)

            if metadata["is_a_spectrum"] != "True":  # verification that provided file is a spectrum
                st.write("Imported file is not valid!")

            initial_value, step = metadata["initial_value"], metadata["step"]

            try:

                temp_mass_list = (mass_string.strip()).split(",")
                mass_list = []  # list of desired molar masses to be displayed on graph
                for element in temp_mass_list:

                    if element.strip() == "ox":
                        mass_list.append("ox")

                    else:
                        mass_list.append(float(element.strip()))

                placeholder = st.empty()
                with placeholder.container():
                    fig, ax = plt.subplots()
                    x = fn.get_time_list(spectrum_list)
                    x_converted = [dt.datetime.fromtimestamp(element) for element in
                                   x]  # convert date and time from computer format to human readable format

                    mass_dictionary = {}  # dictionaty to be displayed in table with numerical values
                    mass_dictionary[f"Time:"] = x_converted  # first column is time moments of measurements

                    for given_mass in mass_list:

                        if given_mass == "ox":
                            y = []
                            for key in oxygen_list:
                                print(oxygen_list[key])
                                y.append(oxygen_list[key])


                        else:
                            mass_number = int((given_mass - initial_value) / step)
                            # st.write(mass_number)
                            try:
                                y = fn.plot_mass(spectrum_list, mass_number, isppm)
                            except:
                                pass

                        display_range = y

                        if isppm == "True" or given_mass == "ox":
                            ylabel = "PPM"
                        else:
                            ylabel = "Pascal"

                        if islogarithmic == "True":

                            new_range = []

                            for element in display_range:
                                if element < 0:
                                    element = 0 - element
                                element += 1

                                new_range.append(math.log(element, 10))
                            display_range = new_range
                            ylabel = f'log10 {ylabel}'

                        ax.plot(x_converted, display_range, label=f"M: {given_mass}")
                        ax.set_ylabel(ylabel)
                        mass_dictionary[f"M = {str(given_mass)}"] = y

                    ax.set_xlabel(f'Time')
                    ax.set_ylabel(ylabel)
                    ax.legend()
                    ax.set_title(f'{ylabel} vs time for given M')

                    # ax.xaxis.axis_date(tz=None)

                    st.pyplot(fig)

                    do_display_table = st.button(
                        label="display table with values")  # optionally display table with numerical values
                    if do_display_table:
                        st.write(pd.DataFrame(mass_dictionary))
            except:
                pass




        except:
            st.write(f"Can't read spectrums from {spectrum_name}")
