from GUI_File_Manager import FindAllSpectrums
import streamlit as st
import os
import JSONoperators as js

def DeleteUnusedFiles(MainConfig="MainConfig"):
    Spectrum_List = FindAllSpectrums(MainConfig)
    for filename in Spectrum_List:
        delete_button = st.button(f"Permanently delete {filename}")
        if delete_button:
            try:
                os.system(f"rm {filename}")
            except:
                st.write(f"{filename} already deleted")

    delete_main_log = st.button(f"Clean main log")
    if delete_main_log:
        log_name = js.ReadJSONConfig("log","MainLog")
        try:
            os.system(f"rm {log_name}")
        except:
            st.write("Log alrealy cleaned")

    delete_abnorm_log = st.button(f"Clean abnormality log")
    if delete_abnorm_log:
        try:
            os.system(f"rm AbnormalityLog")
        except:
            st.write("Abnormality log already cleaned")

    delete_vsc_log = st.button(f"Clean VSC log")
    if delete_vsc_log:
        try:
            os.system(f"rm VSC_log")
        except:
            st.write("VSC log already cleaned")




    delete_main_config = st.button(f"Reset config")
    if delete_main_config:
        try:
            os.system(f"rm MainConfig")
        except:
            st.write("Config already reseted")


if __name__ == "__main__":
    DeleteUnusedFiles()