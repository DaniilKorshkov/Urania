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





def vsc_graphs(log_dictionary):  # function to display plots for constant masses with time on X axis and PPM on Y axis


    

    placeholder = st.empty()
    with placeholder.container():
        fig, ax = plt.subplots()

        #mass_dictionary = {}  # dictionaty to be displayed in table with numerical values
        #mass_dictionary[f"Time:"] = x_converted   # first column is time moments of measurements
        
        
        x = fn.get_time_list(spectrum_list)
        x_converted = [dt.datetime.fromtimestamp(element) for element in x]
        y_mfc_flow = []

        for key in x:

            y_mfc_flow.append(log_dictionary[str(key)])


    


        ax.plot(x_converted, y_mfc_flow, label=f"M: {given_mass}")
        ax.set_ylabel(ylabel)
        mass_dictionary[f"M = {str(given_mass)}"] = y


        ax.set_xlabel(f'Time')
        ax.set_ylabel("MFC flow")
        ax.legend()
        ax.set_title(f'MFC flow vs time for given M')

        #ax.xaxis.axis_date(tz=None)

        st.pyplot(fig)

        do_display_table = st.button(label="display table with values")  # optionally display table with numerical values
        if do_display_table:
            st.write(pd.DataFrame(log_dictionary))
            
            

def display_data():
    
    
    parsing_mode = st.selectbox("Parsing mode",["last","search"])
    st.write(f"{parsing_mode} mode of operation")

    if parsing_mode == "search":  #get desired moment of time is parsing mode is search
        #time_moment = st.text_input("Moment of time to search for: ")
        #time_moment = int(date_time_input())

        select_mode = st.selectbox(label="Select how to get time input: ",options=("Current","Default","Select"))

        match select_mode:
            case "Current":
                time_moment = int((datetime.datetime.now()).timestamp())
            case "Select":
                time_moment = int(date_time_input())



        st.write(f"Time = {dt.datetime.fromtimestamp(time_moment)}")
        
    
    howmuchspectrums = st.text_input(label="How much spectrums to display: ")  # user is prompted to override amount of displayed spectrums
    if howmuchspectrums == "":
        howmuchspectrums = 10
    
    howmuchspectrums = int(howmuchspectrums) # assert that howmuchspectrums is int and greater than 0
    assert howmuchspectrums > 0
    
    if parsing_mode == "last":
            log_dictionary = js.read_last_vsc_entries(howmuchspectrums)   # most recent spectrums are imported from JSON file
    else:
            log_dictionary = js.read_vsc_period_of_time(howmuchspectrums,time_moment)
    
    vsc_graph(log_dictionary)
    
    
display_data()


