import RGA_comms as rga
import streamlit as st

changeip = st.button("Netdiscover for RGA IP")
if changeip:
    rga.change_rga_ip("MainConfig")