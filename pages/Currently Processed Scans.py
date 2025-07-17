import json
import StreamlitGUI as sg
import JSONoperators as js
import streamlit as st
import datetime as dt
from StreamlitGUI import date_time_input, TimeInputWidget
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
import matplotlib.ticker as ticker

def GetFileList():

    FileList = []

    handle = open("TaskList","r")
    for line in handle:
        
        try:
            dictline = json.loads(line)

            if dictline["class"] == "task":

                filename = dictline["filename"]
                #st.write(filename)
                if not (filename in FileList):
                    FileList.append(filename)

        except:
            pass

    return FileList



def DisplayCurrentScans():
    filelist = GetFileList()

    st.write(f"Reading following files: {filelist}")

    default_mass_string = js.ReadJSONConfig("cache", "default_mass_string")
    isinterpreted = st.radio(f"Do interpret spectra?", ["True", "False"])
    if isinterpreted == "False":

        st.write(f"Enter desired M/Z separated by comma: (default: {default_mass_string}) ")
        mass_string = st.text_input(label="Enter desired M/Z (or 'ox') separated by comma: ")
        if mass_string == "":
            mass_string = default_mass_string  # user is promted to input list of desired masses as string. If nothing is inputed, default list is used

        temp_mass_list = (mass_string.strip()).split(",")
        mass_list = []  # list of desired molar masses to be displayed on graph

    islogarithmic = st.radio(f"Do display logarithmic scalе?", ["True", "False"])
    isppm = st.radio(f"Do convert to ppm?", ["True", "False"])
    
    

    


    howmuchspectrums = TimeInputWidget()




    howmuchspectrums = int(howmuchspectrums)  # assert that howmuchspectrums is int and greater than 0

    assert howmuchspectrums > 0

    parsing_mode = st.selectbox("Parsing mode", ["last", "search"])

    st.write(f"{parsing_mode} mode of operation")

    if parsing_mode == "search":  # get desired moment of time is parsing mode is search
        # time_moment = st.text_input("Moment of time to search for: ")
        # time_moment = int(date_time_input())

        select_mode = st.selectbox(label="Select how to get time input: ", options=("Select", "Current"))

        match select_mode:
            case "Current":
                time_moment = int((dt.datetime.now()).timestamp())

            case "Select":
                time_moment = int(date_time_input())

        st.write(f"Time = {dt.datetime.fromtimestamp(time_moment)}")

    for spectrum_name in filelist:

        st.write(f"Reading logs from {str(spectrum_name)} source")

        # time_moment = Settings["default_moment_of_time"]

        try:

            if parsing_mode == "last":
                metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = js.read_last_spectrums_for_time(spectrum_name,
                                                                              howmuchspectrums)  # most recent spectrums are imported from JSON file
            else:
                metadata, spectrum_list, oxygen_list, custom_names_list, solutions_list = js.read_period_of_time_wrt_time(spectrum_name, howmuchspectrums,time_moment)

            
            if spectrum_list == None or len(spectrum_list) == 0:
                st.write(f"No data had been recorded yet")
            else:
                                                                              

                if metadata["is_a_spectrum"] != "True":  # verification that provided file is a spectrum
                    st.write("Imported file is not valid!")

                initial_value, step = metadata["initial_value"], metadata["step"]

                try:

                    if isinterpreted == "False":


                        temp_mass_list = (mass_string.strip()).split(",")


                        mass_list = []  # list of desired molar masses to be displayed on graph
                        for element in temp_mass_list:

                            if element.strip() == "ox":
                                mass_list.append("ox")
                                # st.write(type(len(spectrum_list[0])))

                            else:
                                try:
                                    float_mass = float(element.strip())

                                    temp_timestamp = list(spectrum_list)[0]
                                    if (float_mass < initial_value) or (
                                            float_mass > (initial_value + step * (len(spectrum_list[temp_timestamp])) - 1)):
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

                                        ax.plot(x_converted, display_range, label=f"M/Z: {given_mass}")

                                        mass_dictionary[f"M/Z = {str(given_mass)}"] = y


                        if isppm == "True":
                            ylabel = "PPM"
                        else:
                            ylabel = "ATM"

                        

                        if (islogarithmic == "True" and isppm == "True"):
                            ax.set_yscale('symlog')
                            ax.set_ylim([1, 2000000])
                        elif (islogarithmic == "True" and isppm == "False"):
                            ax.set_yscale('symlog')
                            ax.set_ylim([1, 500000000])




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







                    

                    
                        


                    


                    ax.set_xlabel(f'Time')
                    ax.set_ylabel(ylabel)


                    ax.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
                    ax.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

                    ax.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
                    ax.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)


                    ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
                    ax.tick_params('x', labelrotation=90)

                    ax.legend()
                    ax.set_title(f'{ylabel} vs time for given M')

                    # ax.xaxis.axis_date(tz=None)

                    st.pyplot(fig)

                    do_display_table = st.button(
                        label=f"display table with values for {spectrum_name}")  # optionally display table with numerical values
                    if do_display_table:
                        st.write(pd.DataFrame(mass_dictionary))
                except:
                    pass




        except:
            st.write(f"Can't read spectrums from {spectrum_name}")



    find_abnormalities = st.button("Find abnormalities")
    if find_abnormalities:
        if_abnormalities_found_in_all_files = False
        for filename in filelist:
            spectrum_filename = filename
            if_abnormalities, log_entries_list = ar.AnalyzeInterpretedFile(spectrum_filename)
            if if_abnormalities:
                for element in log_entries_list:
                    st.write(element)
                    if_abnormalities_found_in_all_files = True
        if not if_abnormalities_found_in_all_files:
            st.write("No abnormalities found in these files")





DisplayCurrentScans()