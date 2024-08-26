from duplicity.config import timeout

import RGA_comms as rga
import streamlit as st




heatstat, capheatstat, pumpstat = rga.heating_info("MainConfig")



st.write(f"Pump status: {pumpstat}")
col1,col2 = st.columns(2)

with col1:
    pumpoff = st.button("Pump Off")
with col2:
    pumpon = st.button("Pump On")


st.write(f"Capillary heater status: {capheatstat}")
col1,col2 = st.columns(2)
with col1:
    choff = st.button("Capillary Heater Off")
with col2:
    chon = st.button("Capillary Heater On")



st.write(f"Heater status: {heatstat}")
col1,col2,col3 = st.columns(3)
with col1:
    heatoff = st.button("Heater Off")
with col2:
    heatwarm = st.button("Heater On")
with col3:
    heatbake = st.button("Heater Bake")




if pumpoff:
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



data_type = st.radio("Select data type to inquire: ",["Info","EGains","InletInfo","RFInfo","MultiplierInfo","SourceInfo","DetectorInfo","FilamentInfo","TotalPressureInfo","AnalogInputInfo","AnalogOutputInfo","DigitalInfo","RolloverInfo","RVCInfo","CirrusInfo"])
inquire = st.button("Inquire")
if inquire:
    ret, void = rga.SendPacketsToRGA([data_type])
    splitret = ret[0].split("\n")
    for element in splitret:
        st.write(element)







