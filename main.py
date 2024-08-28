import streamlit as st   #main page of webapp. Right now it is effectively a placeholder

import RGA_comms as rc
import StreamlitGUI as sg
import JSONoperators as js
import datetime


st.write("Welcome to Urania sampling system graphic user interface")
st.markdown("")
st.write("Use pages on the sidebar to the left to inspect data readings from different sources")
st.write("Use SettingsPage to change settings of each data visualisation page")
st.write("Use SpectrumsManager page to list all spectrum files and inspect metadata")
st.write("Use Task Manager to inspect, add or remove tasks for sampling system")
st.write("Use VSC page to read data and manually control vacuum control system and multi-inlet valve")
st.write("Use Technical page to find RGA IP address")
st.write("Use RGA Controls page to control pump, heater and capillary heater; and to inquire data from RGA")
for i in range(10):
    st.markdown("")
st.write("https://github.com/DaniilKorshkov/Urania")
st.write("Carleton University Physics Department")
st.write("Licensed under GNU GPL v3.0. No rights reserved")