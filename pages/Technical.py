import RGA_comms as rga
import streamlit as st
import usb_autolocator

changeip = st.button("Netdiscover for RGA IP")
st.write("Please unplug VSC, oxygen analyzer and multi inlet valve from computer before allocating addresses")
usb_discovery = st.button("Locate devices on USB bus")

if changeip:
    rga.change_rga_ip("MainConfig")
if usb_discovery:
    usb_autolocator.allocate_usb_devices()