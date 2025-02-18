import streamlit as st   #main page of webapp. Right now it is effectively a placeholder

import RGA_comms as rc
import StreamlitGUI as sg
import JSONoperators
import datetime


JSONoperators.MergeJSONConfigs("MainConfig","DefaultMainConfig")

st.write("Welcome to Urania sampling system graphic user interface")
st.markdown("")
st.write("Use Currently Processed Scans page on the sidebar to the left to inspect all data currently recorded")
st.write("Use Abnormality Settings page to change PPM threshold, beyond which readings are considered abnormal")
st.write("Use Manually Inspect Spectrum page to inspect specific data file")
st.write("Use SettingsPage to change settings of 'Manually Inspect Spectrum' page")
st.write("Use SpectrumsManager page to list all spectrum files; inspect metadata and create new files")
st.write("Use Task Manager to inspect, add or remove tasks for the sampling system")
st.write("Use VSC page to manually control vacuum control system and multi-inlet valve")
st.write("Use Technical page to find RGA IP address, and locate VSC, MIV and OA on USB bus")
st.write("Use RGA Controls page to control pump, heater and capillary heater; and to inquire technical data from RGA")
for i in range(10):
    st.markdown("")
st.write("https://github.com/DaniilKorshkov/Urania")
st.write("Carleton University Physics Department")
st.write("Licensed under GNU GPL v3.0. No rights reserved")