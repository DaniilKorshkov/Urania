import os

import streamlit as st
import subprocess
from JSONoperators import ReadJSONConfig
import json
import stat




def if_file_is_spectrum(filename):
    try:
        handle = open(f"{filename}","r")
        for line in handle:
            dictline = json.loads(line)
            if dictline["class"] == "metadata" and dictline["is_a_spectrum"] == "True":
                return True
                break
        handle.close()
        return False

    except:
        return False



def FindAllSpectrums(MainConfig="MainConfig"):
    

    ret = str((subprocess.run(f"ls",capture_output=True)).stdout)

    ret = ret.strip("b")
    ret = ret.strip("'")

    files_list = ret.split("\\n")
    final_files_list = []

    for file in files_list:
        if if_file_is_spectrum(file):
            final_files_list.append(file)

    return final_files_list


def GUI_File_Info(filename,MainConfig="MainConfig"):
    handle = open(filename,"r")
    for line in handle:
        dictline = json.loads(line)
        if dictline["class"] == "metadata":
            valve = dictline["valve_number"]
            init_scan = dictline["initial_value"]
            amt_of_scans = dictline["amount_of_scans"]
            step = dictline["step"]
            return f"{str(filename)} parameters: \nValve:{valve}; Initial M:{init_scan}, amount of scans:{amt_of_scans}, step:{step}"


def CreateSpectrum(filelist, MainConfig="MainConfig"):

    first_line = {"class":"metadata","is_a_spectrum":"True"}

    name = st.text_input(label="Type new spectrum name")
    valve = st.text_input(label="Type multi inlet valve position")
    init_m = st.text_input(label="Type initial M")
    scans = st.text_input(label="Type amount of scans")
    step = st.text_input(label="Type step")

    create_new_spectrum = st.button("Create spectrum")
    if create_new_spectrum:
        try:
            valve = int(valve)
            assert valve >=1 and valve <= 16

            assert not(name in filelist)

            init_m = float(init_m)
            scans = int(scans)
            step = float(step)

            first_line["valve_number"] = valve
            first_line["initial_value"] = init_m
            first_line["amount_of_scans"] = scans
            first_line["step"] = step

            line = json.dumps(first_line)


            handle = open(name,"w")
            handle.close()

            os.system(f"sudo chmod 777 {name}")

            '''ret = str((subprocess.run(f"whoami", capture_output=True)).stdout)
            ret = ret.strip("b")
            ret = ret.strip("'")

            os.system(f"sudo chown {ret}")'''

            handle = open(name, "w")
            handle.write(line)
            handle.close()

            os.system(f"sudo chmod 777 {name}")



        except:
            st.write(f"Input is invalid or name already used")






def SpectrumFileManager(MainConfig="MainConfig"):
    filelist = FindAllSpectrums(MainConfig)
    st.write("Parameters of all spectrum files:")
    st.markdown("")
    for file in filelist:
        try:
            line = GUI_File_Info(file,MainConfig)
            st.write(line)
        except:
            pass


    for i in range(4):
        st.markdown("")

    st.write("Create new spectrum file:")
    CreateSpectrum(filelist,MainConfig)






