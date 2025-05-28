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


def date_time_input():  # function to input date and time as seconds from 01jan1970 through graphic user interface

    col = st.columns((1, 1), gap='medium')  # left part of the screen to input date, right - to input time
    with col[0]:
        date_value = st.date_input(label="Enter date: ", min_value=datetime.date(1969, 1, 1))
    with col[1]:
        time_value = st.time_input(label="Enter time: ")

    date_value = str(date_value)  # obtained results converted to strings and then split into integers
    time_value = str(time_value)

    date_array = date_value.split("-")
    time_array = time_value.split(":")

    # print(date_array)
    # print(time_array)

    datetime_value = (datetime.datetime(year=int(date_array[0]), month=int(date_array[1]), day=int(date_array[2]),
                                        hour=int(time_array[0]), minute=int(time_array[1]),
                                        second=int(time_array[2]))).timestamp()
    return datetime_value  # integers are merged together using datetime.datetime and then returned


def arduino_graphs(log_dictionary):  # function to display plots for constant masses with time on X axis and PPM on Y axis

    placeholder = st.empty()
    with placeholder.container():
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        fig3, ax3 = plt.subplots()
        fig4, ax4 = plt.subplots()
        fig5, ax5 = plt.subplots()

        # mass_dictionary = {}  # dictionaty to be displayed in table with numerical values
        # mass_dictionary[f"Time:"] = x_converted   # first column is time moments of measurements

        x = fn.get_time_list(log_dictionary)

        x_converted = [dt.datetime.fromtimestamp(element) for element in x]

        y_mfc_flow = []
        y_mfm_flow = []
        y_pg_pressure = []
        y_pc_pressure = []
        y_filling_mfm_flow = []

        for key in x:
            y_mfc_flow.append((log_dictionary[f"{str(key)}"])["mfc_flow"])
            y_mfm_flow.append((log_dictionary[f"{str(key)}"])["mfm_flow"])
            y_pg_pressure.append((log_dictionary[f"{str(key)}"])["pg_pressure"])
            y_pc_pressure.append((log_dictionary[f"{str(key)}"])["pc_pressure"])
            y_filling_mfm_flow.append((log_dictionary[f"{str(key)}"])["filling_mfm_flow"])

        ax1.plot(x_converted, y_mfc_flow)
        ax1.set_xlabel(f'Time')
        ax1.set_ylabel("MFC flow (cm3/min)")
        ax1.set_title(f'MFC flow (cm3/min) vs time')

        ax1.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
        ax1.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

        ax1.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax1.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax1.xaxis.set_major_locator(ticker.MaxNLocator(5))
        ax1.tick_params('x', labelrotation=90)
        ax1.legend()

        st.pyplot(fig1)

        ax2.plot(x_converted, y_mfm_flow)
        ax2.set_xlabel(f'Time')
        ax2.set_ylabel("MFM flow (cm3/min)")
        ax2.set_title(f'MFM flow (cm3/min) vs time')

        ax2.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
        ax2.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

        ax2.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax2.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax2.xaxis.set_major_locator(ticker.MaxNLocator(5))
        ax2.tick_params('x', labelrotation=90)
        ax2.legend()

        st.pyplot(fig2)

        ax3.plot(x_converted, y_pg_pressure)
        ax3.set_xlabel(f'Time')
        ax3.set_ylabel("PT pressure (torr)")
        ax3.set_title(f'PT pressure (torr) vs time')

        ax3.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
        ax3.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

        ax3.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax3.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax3.xaxis.set_major_locator(ticker.MaxNLocator(5))
        ax3.tick_params('x', labelrotation=90)
        ax3.legend()

        st.pyplot(fig3)

        ax4.plot(x_converted, y_pc_pressure)
        ax4.set_xlabel(f'Time')
        ax4.set_ylabel("PC pressure (torr)")
        ax4.set_title(f'PC pressure (torr) vs time')

        ax4.xaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)
        ax4.yaxis.grid(which='major', color='k', alpha=0.8, linestyle='--', linewidth=1)

        ax4.xaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax4.yaxis.grid(which='minor', color='k', alpha=0.5, linestyle=':', linewidth=0.75)
        ax4.xaxis.set_major_locator(ticker.MaxNLocator(5))
        ax4.tick_params('x', labelrotation=90)
        ax4.legend()

        st.pyplot(fig4)

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

        do_display_table = st.button(
            label="display table with values")  # optionally display table with numerical values
        if do_display_table:

            converted_log_dictionary = {}
            for key in log_dictionary:
                converted_log_dictionary[dt.datetime.fromtimestamp(int(key))] = log_dictionary[key]

            st.write(pd.DataFrame(converted_log_dictionary))


def display_data():
    js.assert_file_exists("arduino_log")

    parsing_mode = st.selectbox("Parsing mode", ["last", "search"])
    st.write(f"{parsing_mode} mode of operation")

    if parsing_mode == "search":  # get desired moment of time is parsing mode is search
        # time_moment = st.text_input("Moment of time to search for: ")
        # time_moment = int(date_time_input())

        time_moment = int(date_time_input())

        st.write(f"Time = {dt.datetime.fromtimestamp(time_moment)}")

    howmuchspectrums = TimeInputWidget()

    howmuchspectrums = int(howmuchspectrums)  # assert that howmuchspectrums is int and greater than 0
    assert howmuchspectrums > 0

    if parsing_mode == "last":
        log_dictionary = js.read_last_vsc_entries_wrt_time(
            howmuchspectrums)  # most recent spectrums are imported from JSON file
    else:
        log_dictionary = js.read_vsc_period_of_time_wrt_time(howmuchspectrums, time_moment)

    arduino_graphs(log_dictionary)

    for i in range(5):
        st.markdown("")




display_data()