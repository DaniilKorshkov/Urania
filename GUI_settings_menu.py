import JSONoperators as js
import streamlit as st
import StreamlitGUI as sg
import json
import datetime



def reset_to_default(settings_filename,default_settings_filename):  # function to reset JSON settings config to factory default

    Settings_List = []  # new settings list is a list of strings of old GUI_settings config to be modified later

    handle = open(default_settings_filename, "r")
    for line in handle:  # copy of factory default confing is made to Settings_List
        Settings_List.append(line)
    handle.close()

    handle = open(settings_filename, "w")
    for line in Settings_List:   # copy is re-written to Settings file
        handle.write(line)
    handle.close()


def apply_page_settings(settings_filename,New_Settings):      # function to change one line in JSON config (settings_filename) to modified one (New_Settings) with respect to selected page




    New_Settings_List = []  #new settings list is a list of strings of old GUI_settings config to be modified later

    handle = open(settings_filename, "r")

    for line in handle:  # old JSON file is copied to New_Settings_List. Old file is to be erased later
            if str(New_Settings["page_name"]) == str((json.loads(line))["page_name"]):
                New_Settings_List.append(json.dumps(New_Settings))  # if page_number in the line of old config equals to page_number in new line, the line is replaced
            else:
                New_Settings_List.append(line)  # else, line is copied

    handle.close()


    handle = open(settings_filename,"w")
    i = 1
    for line in New_Settings_List:
        handle.write(line.strip("\n"))   #GUI_settings config is re-written with formatted New_Settings_List
        if i < len(New_Settings_List):
             handle.write("\n")
        i += 1
    handle.close()





def modify_filename(Settings,settings_file):   # function to change desired filename of spectrum log that page is operating with
    New_Settings = Settings

    old_filename = Settings["spectrum_filename"]

    new_filename = st.text_input(f"Input new filename: ")
    st.write(f"Current filename = {old_filename}")
    do_modify_filename = st.button("Apply new filename")


    if new_filename != "":  # if input us non-zero, program verifies if provided file is a spectrum
        try:
            metadata, placeholder = js.read_spectrum_json(new_filename)

            if str(metadata["is_a_spectrum"]) == str("True"):

                if do_modify_filename:
                    New_Settings["spectrum_filename"] = new_filename  # if file provided exists and is valid, filename is successfully changed

                    apply_page_settings(settings_file,New_Settings)
            else:
                st.write(f"Not a valid file!")  # otherwise, error message is returned
        except:

            st.write(f"No such file found")


def modify_control_spectrum_filename(Settings,settings_file):   # function to change desired filename of spectrum log that page is operating with
    New_Settings = Settings

    old_filename = Settings["control_spectrum_filename"]

    new_filename = st.text_input(f"Input new control spectrum filename: ")
    st.write(f"Current filename = {old_filename}")
    do_modify_filename = st.button("Apply new control spectrum filename")


    if new_filename != "":  # if input us non-zero, program verifies if provided file is a spectrum
        try:
            metadata, placeholder = js.read_spectrum_json(new_filename)

            if str(metadata["is_a_control_spectrum"]) == str("True"):

                if do_modify_filename:
                    New_Settings["control_spectrum_filename"] = new_filename  # if file provided exists and is valid, filename is successfully changed

                    apply_page_settings(settings_file,New_Settings)
            else:
                st.write(f"Not a valid file!")  # otherwise, error message is returned
        except:

            st.write(f"No such file found")





def modify_parsing_mode(Settings,settings_file):  #function to change defaults parsing mode (show most recent spectrums or look for given period of time)
    New_Settings = Settings

    old_mode = Settings["parsing_mode"]

    new_mode = st.radio(f"Select default parsing mode", ["last", "search"])
    st.write(f"Current parsing mode = {old_mode}")
    do_modify_mode = st.button("Apply new mode")
    if do_modify_mode:
        New_Settings["parsing_mode"] = new_mode

        apply_page_settings(settings_file, New_Settings)

def modify_default_time_moment(Settings,settings_file):   # function to modify default time moment for searching parsing mode

    New_Settings = Settings

    new_moment = sg.date_time_input()
    old_moment = Settings["default_moment_of_time"]
    #print(f"Current default time = {datetime.datetime.fromtimestamp(old_moment)}")

    do_modify_time_moment = st.button("Apply new time moment")
    if do_modify_time_moment:


            New_Settings["default_moment_of_time"] = new_moment
            apply_page_settings(settings_file, New_Settings)




def modify_orientation(Settings,settings_file):  # function to select horizontal or vertical orientation of page
    New_Settings = Settings

    new_orientation = st.radio(f"Select orientation",["vertical","horizontal"])
    old_option = Settings["orientation"]
    st.write(f"Current orientation = {old_option}")
    do_modify_orientation = st.button("Apply new orientation")
    if do_modify_orientation:
        New_Settings["orientation"] = new_orientation

        apply_page_settings(settings_file,New_Settings)


def modify_default_amount_of_spectrums(Settings,settings_file):    # function to change default amount of spectrums that page is displaying
    New_Settings = Settings

    new_amount = st.text_input(f"Input new default amount of spectrums: ")
    old_option = Settings["default_amount_of_spectrums"]
    st.write(f"Current amount of spectrums displayed = {old_option}")
    do_modify_amount = st.button("Apply new default amount")

    try:
        placeholder = int(new_amount)  #required to verify that input value is integer and is greater than zero. If those conditions are not satisfied, JSON config is not changed
        assert placeholder > 0

        if do_modify_amount:
            New_Settings["default_amount_of_spectrums"] = new_amount

            apply_page_settings(settings_file,New_Settings)
    except:
        pass


def modify_default_mass_list(Settings,settings_file):   # function to change array of masses that are displayed on const_mass plot by default
    New_Settings = Settings

    new_masses = st.text_input(f"Input new default masses for constant time chart: ")
    old_option = Settings["default_masses"]
    st.write(f"Current mass list = {old_option}")
    do_modify_masses = st.button("Apply new default masses")

    try:
        placeholder_array = new_masses.split(",")
        for element in placeholder_array:
            element2 = float(element)

        if do_modify_masses:
            New_Settings["default_masses"] = new_masses

            apply_page_settings(settings_file,New_Settings)

    except:
        pass


def modify_do_display_3d(Settings,settings_file):  # function to turn on or off 3d plot
    New_Settings = Settings

    new_3d = st.radio(f"Do display 3d chart?", ["True", "False"])
    old_option = Settings["do_display_3d"]
    st.write(f"Current option = {old_option}")
    do_modify_3d = st.button("Apply new option")
    if do_modify_3d:
        New_Settings["do_display_3d"] = new_3d

        apply_page_settings(settings_file,New_Settings)


def modify_do_display_const_mass(Settings,settings_file): # function to turn on or off const_mass plot
    New_Settings = Settings

    new_3d = st.radio(f"Do display constant mass chart?", ["True", "False"])
    old_option = Settings["do_display_const_mass"]
    st.write(f"Current option = {old_option}")
    do_modify_const_mass = st.button("Apply new option1")
    if do_modify_const_mass:
        New_Settings["do_display_const_mass"] = new_3d

        apply_page_settings(settings_file,New_Settings)


def modify_do_display_const_time(Settings,settings_file): # function to turn on or off const_time spectrum
    New_Settings = Settings

    new_3d = st.radio(f"Do display constant time chart?", ["True", "False"])
    old_option = Settings["do_display_const_time"]
    st.write(f"Current option = {old_option}")
    do_modify_3d = st.button("Apply new option2")
    if do_modify_3d:
        New_Settings["do_display_const_time"] = new_3d

        apply_page_settings(settings_file,New_Settings)










def Settings_Menu(settings_file, default_settings_file):                          #ready to use settings menu
    page_list = js.read_all_page_numbers(settings_file)

    if len(page_list) > 1:
        page_selection = st.slider(label="Select page to modify settings",min_value=1,max_value=(len(page_list)))
    else:
        page_selection = 1

    st.write(f"Settings for page #{page_selection}")

    Settings = js.read_GUI_page_settings(settings_file, str(page_selection))

    modify_filename(Settings,settings_file)  # all options are displayed sequentially with 6 gaps in between
    for i in range(6):
        st.markdown("")
    modify_control_spectrum_filename(Settings, settings_file)
    for i in range(6):
        st.markdown("")
    modify_parsing_mode(Settings,settings_file)
    for i in range(6):
        st.markdown("")
    st.write(f"Choose default moment of time for 'Search' parsing mode")
    modify_default_time_moment(Settings, settings_file)
    for i in range(6):
        st.markdown("")
    modify_orientation(Settings,settings_file)
    for i in range(6):
        st.markdown("")
    modify_default_amount_of_spectrums(Settings,settings_file)
    for i in range(6):
        st.markdown("")
    modify_default_mass_list(Settings,settings_file)
    for i in range(6):
        st.markdown("")
    modify_do_display_3d(Settings,settings_file)
    for i in range(6):
        st.markdown("")
    modify_do_display_const_mass(Settings,settings_file)
    for i in range(6):
        st.markdown("")
    modify_do_display_const_time(Settings,settings_file)
    for i in range(6):
        st.markdown("")

    reset_settings = st.button(label="reset all settings to default")
    if reset_settings:
        reset_to_default(settings_file,default_settings_file)







