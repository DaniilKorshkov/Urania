import streamlit as st
import pandas as pd
import pickle as pk
import numpy as np
import matplotlib.pyplot as plt
import Functions as fn
import datetime as dt

import JSONoperators
import JSONoperators as js
import datetime
import streamlit.components.v1 as components
import math
import AbnormalityReaction as ar
import GUI_File_Manager as fm
import matplotlib.ticker as ticker
import json
from StreamlitGUI import TimeInputWidget
from StreamlitGUI import date_time_input








def vsc_graphs(log_dictionary):  # function to display plots for constant masses with time on X axis and PPM on Y axis


    

    placeholder = st.empty()
    with placeholder.container():
        
        fig5, ax5 = plt.subplots()


        ax5.plot(x_converted, y_filling_mfm_flow)
        ax5.set_xlabel(f'Time')
        ax5.set_ylabel("Filling station flow (cm3/min)")
        ax5.set_title(f'Filling station flow (cm3/min) vs time')

        ax5.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
        ax5.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

        ax5.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax5.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax5.xaxis.set_major_locator(ticker.MaxNLocator(5))
        ax5.tick_params('x', labelrotation=90)
        ax5.legend()

        st.pyplot(fig5)














        do_display_table = st.button(label="display table with values for VSC")  # optionally display table with numerical values
        if do_display_table:

            converted_log_dictionary = {}
            for key in log_dictionary:
                converted_log_dictionary[dt.datetime.fromtimestamp(int(key))] = log_dictionary[key]

            st.write(pd.DataFrame(converted_log_dictionary))
            








def manually_compute_filled_volume(MainConfig="MainConfig"):


    init_time = date_time_input(self_name = "Initial time")
    final_time = date_time_input(self_name = "Final time")


    st.write(f"Initial time: {datetime.datetime.fromtimestamp(init_time)}")
    st.write(f"Final time: {datetime.datetime.fromtimestamp(final_time)}")

    integral = JSONoperators.filling_numerical_integration(init_time,final_time)

    st.write(f"Filled amount: {integral} liters")






def display_filling_counters(MainConfig="MainConfig"):
    js.assert_file_exists("FillingCounters")
    counter_list = []

    handle = open("FillingCounters", "r")
    for line in handle:
        if line == None or line == "" or line == "\n":
            pass
        else:
            counter_list.append(line)
    handle.close()

    for line in counter_list:
        dictline = json.loads(line)
        name = dictline["name"]
        st.write(name)
        init_time = dictline["initial_time"]
        try:
            final_time = dictline["final_time"]
            st.write(f"Initial time: {datetime.datetime.fromtimestamp(init_time)}")
            st.write(f"Final time: {datetime.datetime.fromtimestamp(final_time)}")

            integral = JSONoperators.filling_numerical_integration(init_time,final_time)

            st.write(f"Filled amount: {integral} liters")


        except:
            final_time = int(datetime.datetime.now().timestamp())
            st.write(f"Initial time: {datetime.datetime.fromtimestamp(init_time)}")
            st.write(f"Currently filling...")

            integral = JSONoperators.filling_numerical_integration(init_time, final_time)

            st.write(f"Filled amount: {integral}")


            stop_counter = st.button(f"Stop {name} counter")


            if stop_counter:

                newfile = []

                handle = open("FillingCounters", "r")
                for handleline in handle:

                    if handleline == None or handleline == "" or handleline == "\n":
                        pass
                    else:

                        if json.loads(handleline)["name"] == dictline["name"]:

                            dictline["final_time"] = int(datetime.datetime.now().timestamp())

                            newfile.append(str(json.dumps(dictline))+"\n")


                        else:
                            newfile.append(handleline)




                handle.close()

                handle = open("FillingCounters", "w")

                for handleline in newfile:
                    handle.write(handleline)
                handle.close()

        delete_counter = st.button(f"Delete {name} counter")
        save_as_txt = st.button(f"Save {name} as text file")

        if delete_counter:
                newfile = []

                handle = open("FillingCounters", "r")
                for handleline in handle:

                    if handleline == None or handleline == "" or handleline == "\n":
                        pass
                    else:

                        if json.loads(handleline)["name"] == dictline["name"]:

                            pass


                        else:
                            newfile.append(handleline)

                handle.close()

                handle = open("FillingCounters", "w")

                for handleline in newfile:
                    handle.write(handleline)
                handle.close()


        if save_as_txt:

            current_date = dt.datetime.now()
            datetime_label = current_date.strftime("%d_%m_%Y")

            handle = open(f"{name} counter save: {datetime_label}","w")



            handle.write(f"{name} counter: filled {integral} liters since {datetime.datetime.fromtimestamp(init_time)} to {datetime.datetime.fromtimestamp(final_time)}")


            handle.close()
            st.write(f"Saved!")


        for i in range(4):
            st.markdown("")


def create_new_filling_counter(MainConfig="MainConfig"):
    js.assert_file_exists("FillingCounters")

    counter_name = st.text_input("Enter new counter name")
    create_new_counter = st.button("Create new counter")

    if create_new_counter:

        newfile = []
        namelist = []
        new_counter_data = {}
        new_counter_data["name"] = counter_name
        new_counter_data["initial_time"] = int(datetime.datetime.now().timestamp())

        handle = open("FillingCounters", "r")
        for line in handle:

            if line == None or line == "" or line == "\n":
                pass
            else:

                newfile.append(line)
                try:
                    namelist.append(json.loads(line)["name"])
                except:
                    pass
        handle.close()

        newfile.append(str(json.dumps(new_counter_data)))





        if (counter_name != "") and not(counter_name in namelist):

            handle = open("FillingCounters", "w")

            for line in newfile:

                if line == None or line == "" or line == "\n":
                    pass
                else:

                    line.strip("\n")
                    handle.write(f"{line}\n")
            handle.close()

        else:
            st.write("Counter with this name already exists")
















def display_data():
    

    js.assert_file_exists("VSC_log")
    js.assert_file_exists("arduino_log")

    parsing_mode = st.selectbox("Parsing mode",["last","search"])
    st.write(f"{parsing_mode} mode of operation")

    if parsing_mode == "search":  #get desired moment of time is parsing mode is search
        #time_moment = st.text_input("Moment of time to search for: ")
        #time_moment = int(date_time_input())


        time_moment = int(date_time_input())



        st.write(f"Time = {dt.datetime.fromtimestamp(time_moment)}")
        
    
    howmuchspectrums = TimeInputWidget()
    
    howmuchspectrums = int(howmuchspectrums) # assert that howmuchspectrums is int and greater than 0
    assert howmuchspectrums > 0
    
    if parsing_mode == "last":
            log_dictionary = js.read_last_vsc_entries_wrt_time(howmuchspectrums)   # most recent spectrums are imported from JSON file
            
    else:
            log_dictionary = js.read_vsc_period_of_time_wrt_time(howmuchspectrums,time_moment)
            
    if len(log_dictionary) > 0:
        vsc_graphs(log_dictionary)
    else:
        st.write("No VSC data recorded yet")


    for i in range(3):
        st.markdown("")


    st.write("Filling counters:")

    for i in range(5):
        st.markdown("")

    display_filling_counters("MainConfig")
    create_new_filling_counter("MainConfig")
    manually_compute_filled_volume("MainConfig")

    
    
display_data()