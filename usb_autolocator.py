import oxygen_analyzer as ox
import VSC_comms as vsc
import subprocess
import JSONoperators as js
import streamlit as st
import json
import time

def find_usb_connections():         # function that returns a list of all ttyUSB* elements in /deb
    ttyUSB_list = []
    ret = subprocess.check_output("ls",cwd="/dev",)
    ret = str(ret)
    allUSB_list = ret.split("\\n")

    #print(allUSB_list)

    #print("456")
    '''for element in allUSB_list:
        print(element)
        if "ttyUSB" in element:
            ttyUSB_list.append(element)'''


    return allUSB_list


def check_for_new_connections():
    old_usb_list = find_usb_connections()
    while True:
        new_usb_list = find_usb_connections()
        if old_usb_list == new_usb_list:
            pass
        else:
            for element in new_usb_list:
                if not (element in old_usb_list) and ("ttyUSB" in element):
                    return element
            break



def allocate_usb_devices():
    st.write("Please plug VSC to USB port")
    vsc_address = check_for_new_connections()
    st.write("VSC address found")
    time.sleep(1)
    st.write("Please plug multi inlet valve to USB port")
    miv_address = check_for_new_connections()
    st.write("Multi inlet valve address found")
    time.sleep(1)
    st.write("Please plug oxygen analyzer to USB port")
    oxa_address = check_for_new_connections()
    st.write("Oxygen analyzer address found")
    time.sleep(1)
    st.write("Please plug Arduino board to USB port")
    arduino_address = check_for_new_connections()
    st.write("Arduino address found")


    handle = open("MainConfig", "r")
    newconfig = []
    for line in handle:
        try:
            dictline = json.loads(line)

            if dictline["class"] == "vicimotor":
                dictline["address"] = f"ASRL/dev/{miv_address}::INSTR"
                newline = json.dumps(dictline)
                newconfig.append(newline + "\n")

            elif dictline["class"] == "ox_an":
                dictline["port"] = f"/dev/{oxa_address}"
                newline = json.dumps(dictline)
                newconfig.append(newline + "\n")

            elif dictline["class"] == "vsc":
                dictline["vsc_serial_port"] = f"/dev/{vsc_address}"
                newline = json.dumps(dictline)
                newconfig.append(newline + "\n")

            elif dictline["class"] == "arduino":
                dictline["port"] = f"/dev/{arduino_address}"
                newline = json.dumps(dictline)
                newconfig.append(newline + "\n")




            else:
                newconfig.append(line)
        except:
            pass
    handle.close()

    handle = open("MainConfig", "w")
    for line in newconfig:
        handle.write(line)
    handle.close()

    st.write("New addresses added to config")
    st.write("You can close this page now")

