import RGA_comms as rga
import streamlit as st
import usb_autolocator

changeip = st.button("Netdiscover for RGA IP")
st.write("Please unplug VSC, oxygen analyzer, multi inlet valve and arduino board from computer before allocating addresses")
usb_discovery = st.button("Locate devices on USB bus")

if changeip:
    if_success, rga_ip = rga.change_rga_ip("MainConfig")
    if if_success:
        st.write(f"RGA IP is found: {rga_ip}")
    else:
        st.write(f"Can't find RGA IP")
if usb_discovery:
    usb_autolocator.allocate_usb_devices()