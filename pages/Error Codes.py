import streamlit as st
import JSONoperators as js
import datetime
from StreamlitGUI import date_time_input
import json

def DisplaySingleErrorCode(error_code, error_code_key):
    st.write(f"Error code {error_code_key}:")
    st.write(error_code["description"])

    
    current_time = int(datetime.datetime.now().timestamp())
    error_code_timeout = error_code["timeout"]

    if error_code_timeout > current_time:
        st.write(f"Error code disabled until {datetime.datetime.fromtimestamp(error_code_timeout)}")


    st.write(f"Enter time until error code is disabled:")
    new_timeout_time = date_time_input()
    update_timeout_time = st.button(f"Update timeout time for code {error_code_key}")
    if update_timeout_time:
        new_config_line = js.ReadJSONConfig("error_codes")
        ((new_config_line["dictionary"])[error_code_key])["timeout"] = new_timeout_time
        dumped_config_line = json.dumps(new_config_line)
        js.EditJSONConfig("error_codes", dumped_config_line)
    enable_error_code = st.button(f"Enable error code {error_code_key}")
    if enable_error_code:
        new_config_line = js.ReadJSONConfig("error_codes")
        ((new_config_line["dictionary"])[error_code_key])["timeout"] = 0
        dumped_config_line = json.dumps(new_config_line)
        js.EditJSONConfig("error_codes", dumped_config_line)

def ErrorCodesPage():

    ErrorCodesDictionary = js.ReadJSONConfig("error_codes", "dictionary")
    for key in ErrorCodesDictionary:
        DisplaySingleErrorCode(ErrorCodesDictionary[key], key)
        for i in range(6):
            st.markdown("")

    


ErrorCodesPage()