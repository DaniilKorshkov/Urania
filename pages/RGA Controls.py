from duplicity.config import timeout

import RGA_comms as rga
import streamlit as st




heatstat, capheatstat, pumpstat = rga.heating_info("MainConfig")  # query RGA for capillary heater status, heater status and pump status
filamentstatus, activefilament = rga.rga_filament_info("MainConfig")



st.write(f"Pump status: {pumpstat}")   # menu that displays pump status and prompts user to change it
col1,col2 = st.columns(2)

with col1:
    pumpoff = st.button("Pump Off")
with col2:
    pumpon = st.button("Pump On")


st.write(f"Capillary heater status: {capheatstat}")  # menu that displays capillary heater status and prompts user to change it
col1,col2 = st.columns(2)
with col1:
    choff = st.button("Capillary Heater Off")
with col2:
    chon = st.button("Capillary Heater On")



st.write(f"Heater status: {heatstat}")  # menu that displays heater status and prompts user to change it
col1,col2,col3 = st.columns(3)
with col1:
    heatoff = st.button("Heater Off")
with col2:
    heatwarm = st.button("Heater On")
with col3:
    heatbake = st.button("Heater Bake")


st.write(f"Active filament {activefilament}, filament status: {filamentstatus}")
#col1,col2 = st.columns(2)
#with col1:
selectfilament1 = st.button("Select filament 1")
selectfilament2 = st.button("Select filament 2")
#with col2:
    #turnonfilament = st.button("Turn on filament")
    #turnofffilament = st.button("Turn off filament")









if pumpoff:                          # link streamlit buttons to respective RGA functions
    rga.control_pump("off")
if pumpon:
    rga.control_pump("on")
if heatoff:
    rga.control_heater("off")
if heatwarm:
    rga.control_heater("warm")
if heatbake:
    rga.control_heater("bake")
if chon:
    rga.control_capillary_heater("on")
if choff:
    rga.control_capillary_heater("off")
if selectfilament1:
    rga.rga_filament_select("1")
if selectfilament2:
    rga.rga_filament_select("2")
#if turnonfilament:
    #rga.rga_filament_control("On")
#if turnofffilament:
    #rga.rga_filament_control("Off")








for i in range(4):
    st.markdown("")


# function to inquire different types of data from RGA (have no idea what it all means)

data_type = st.radio("Select data type to inquire: ",["Info","EGains","InletInfo","RFInfo","MultiplierInfo","SourceInfo","DetectorInfo","FilamentInfo","TotalPressureInfo","AnalogInputInfo","AnalogOutputInfo","DigitalInfo","RolloverInfo","RVCInfo","CirrusInfo"])
inquire = st.button("Inquire")
if inquire:
    ret, void = rga.SendPacketsToRGA([data_type])
    splitret = ret[0].split("\n")
    for element in splitret:
        st.write(element)







