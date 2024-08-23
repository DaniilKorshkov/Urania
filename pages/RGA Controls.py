import RGA_comms as rga
import streamlit as st

col1,col2 = st.columns(2)
with col1:
    pumpoff = st.button("Pump Off")
with col2:
    pumpon = st.button("Pump On")



col1,col2 = st.columns(2)
with col1:
    choff = st.button("Capillary Heater Off")
with col2:
    chon = st.button("Capillary Heater On")




col1,col2,col3 = st.columns(3)
with col1:
    heatoff = st.button("Heater Off")
with col2:
    heatwarm = st.button("Heater On")
with col3:
    heatbake = st.button("Heater Bake")


cirrusinfo = st.button("Cirrus Info")




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






cirrus_info = rga.cirrus_info()
for line in cirrus_info:
    st.write(line)