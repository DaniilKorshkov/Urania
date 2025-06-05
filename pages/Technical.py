import RGA_comms as rga
import streamlit as st
import usb_autolocator
import os

changeip = st.button("Netdiscover for RGA IP")
st.write("Please unplug VSC, oxygen analyzer, multi inlet valve and arduino board from computer before allocating addresses")
usb_discovery = st.button("Locate devices on USB bus")
force_unlock = st.button("Force unlock communication with USB perippherals")

if changeip:
    if_success, rga_ip = rga.change_rga_ip("MainConfig")
    if if_success:
        st.write(f"RGA IP is found: {rga_ip}")
    else:
        st.write(f"Can't find RGA IP")
if usb_discovery:
    usb_autolocator.allocate_usb_devices()


if force_unlock:
    try:
        os.system("rm .OA_USB_LOCK")
    except:
        pass
    try:
        os.system("rm .ARD_USB_LOCK")
    except:
        pass
    try:
        os.system("rm .VSC_USB_LOCK")
    except:
        pass
    try:
        os.system("rm .VICI_USB_LOCK")
    except:
        pass

    
    st.write("USB peripherals force unlocked")