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


def SpectrumsDropdownMenu(MainConfig="MainConfig"):
    final_files_list = FindAllSpectrums(MainConfig)
    ret = st.selectbox("Spectrum file selection menu",final_files_list)
    return ret







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
    init_m = st.text_input(label="Type initial molar mass")
    final_m = st.text_input(label="Type final molar mass")

    #scans = st.text_input(label="Type amount of scans")

    step = st.text_input(label="Type step")


    create_new_spectrum = st.button("Create spectrum")

    if create_new_spectrum:
        spectrum_is_valid = True
        try:
            valve = int(valve)
            assert valve >=1 and valve <= 16
        except:
            spectrum_is_valid = False
            st.write("Valve position is invalid")

        try:
            assert not(name in filelist)
        except:
            spectrum_is_valid = False
            st.write("Spectrum name already exists")

        try:

            init_m = float(init_m)
            step = float(step)
            final_m = float(final_m)
        except:
            spectrum_is_valid = False
            st.write("Not a valid numbers inputed")


        try:
            assert init_m >= 1
        except:
            spectrum_is_valid = False
            st.write("Initial M is less than 1")

        try:
            assert final_m <= 200
        except:
            spectrum_is_valid = False
            st.write("Final M is greater than 200")


        try:
            assert final_m > init_m
        except:
            spectrum_is_valid = False
            st.write("Final M is lesser or equal than initial M")



        try:
            assert step > 0
        except:
            spectrum_is_valid = False
            st.write("Step is less or equal than zero")




        try:
            scans = int((final_m-init_m)/step) + 1
            if scans < 1:
                scans = 1
        except:
            spectrum_is_valid = False
            st.write("Failed to calculate scan amount")

        if spectrum_is_valid:

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






