import streamlit as st   #main page of webapp. Right now it is effectively a placeholder

import RGA_comms as rc
import StreamlitGUI as sg
import JSONoperators as js
import datetime


st.write("Welcome to Urania sampling system graphic user interface")
st.write("Use sidebar to the left to inspect samples from different pipes")
st.write("Use SettingsPage to change settings of each sample page")
st.write("Use SpectrumsManager page to list all spectrum files and inspect metadata")
st.write("Use Task Manager to inspect, add or remove tasks for sampling system")
st.write("Use VSC page to manually override vacuum control system and multi-inlet valve")
for i in range(10):
    st.markdown("")
st.write("Licensed under GNU GPL v3.0. https://github.com/DaniilKorshkov/Urania")