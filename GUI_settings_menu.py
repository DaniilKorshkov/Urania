import JSONoperators as js
import streamlit as st
import json



def reset_to_default(settings_filename,default_settings_filename):

    Settings_List = []  # new settings list is a list of strings of old GUI_settings config to be modified later

    handle = open(default_settings_filename, "r")
    for line in handle:
        Settings_List.append(line)
    handle.close()

    handle = open(settings_filename, "w")
    for line in Settings_List:
        handle.write(line)
    handle.close()


def apply_page_settings(settings_filename,New_Settings):      # function to change one line in JSON config (settings_filename) to modified one (New_Settings) with respect to selected page


    New_Settings_List = []  #new settings list is a list of strings of old GUI_settings config to be modified later

    handle = open(settings_filename, "r")
    for line in handle:
            if str(New_Settings["page_name"]) == str((json.loads(line))["page_name"]):
                New_Settings_List.append(json.dumps(New_Settings))  # if page_number in the line of old config equals to page_number in new line, the line is replaced
            else:
                New_Settings_List.append(line)  # else, line is copied

    handle.close()


    handle = open(settings_filename,"w")
    i = 1
    for line in New_Settings_List:
        handle.write(line.strip("\n"))   #GUI_settings config is re-written
        if i < len(New_Settings_List):
             handle.write("\n")
        i += 1
    handle.close()





def modify_filename(Settings,settings_file):   # function to change desired filename of spectrum log that page is operating with
    New_Settings = Settings

    new_filename = st.text_input(f"Input new filename: ")
    do_modify_filename = st.button("Apply new filename")
    if do_modify_filename:
        New_Settings["spectrum_filename"] = new_filename

        apply_page_settings(settings_file,New_Settings)


def modify_orientation(Settings,settings_file):  # function to select horizontal or vertical orientation of page
    New_Settings = Settings

    new_orientation = st.radio(f"Select orientation",["vertical","horizontal"])
    do_modify_orientation = st.button("Apply new orientation")
    if do_modify_orientation:
        New_Settings["orientation"] = new_orientation

        apply_page_settings(settings_file,New_Settings)


def modify_default_amount_of_spectrums(Settings,settings_file):    # function to change default amount of spectrums that page is displaying
    New_Settings = Settings

    new_amount = st.text_input(f"Input new default amount of spectrums: ")
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
    do_modify_masses = st.button("Apply new default masses")

    try:
        placeholder_array = new_masses.split(",")
        for element in placeholder_array:
            element2 = int(element)

        if do_modify_masses:
            New_Settings["default_masses"] = new_masses

            apply_page_settings(settings_file,New_Settings)

    except:
        pass


def modify_do_display_3d(Settings,settings_file):  # function to turn on or off 3d plot
    New_Settings = Settings

    new_3d = st.radio(f"Do display 3d chart?", ["True", "False"])
    do_modify_3d = st.button("Apply new option")
    if do_modify_3d:
        New_Settings["do_display_3d"] = new_3d

        apply_page_settings(settings_file,New_Settings)


def modify_do_display_const_mass(Settings,settings_file): # function to turn on or off const_mass plot
    New_Settings = Settings

    new_3d = st.radio(f"Do display constant mass chart?", ["True", "False"])
    do_modify_const_mass = st.button("Apply new option1")
    if do_modify_const_mass:
        New_Settings["do_display_const_mass"] = new_3d

        apply_page_settings(settings_file,New_Settings)


def modify_do_display_const_time(Settings,settings_file): # function to turn on or off const_time spectrum
    New_Settings = Settings

    new_3d = st.radio(f"Do display constant time chart?", ["True", "False"])
    do_modify_3d = st.button("Apply new option2")
    if do_modify_3d:
        New_Settings["do_display_const_time"] = new_3d

        apply_page_settings(settings_file,New_Settings)










def Settings_Menu(settings_file, default_settings_file):                          #ready to use settings menu
    page_list = js.read_all_page_numbers(settings_file)

    if len(page_list) > 1:
        page_selection = st.slider(label="Select page to modify settings",max_value=(len(page_list)-1))+1
    else:
        page_selection = 1

    st.write(f"Settings for page #{page_selection}")

    Settings = js.read_GUI_page_settings(settings_file, str(page_selection))

    modify_filename(Settings,settings_file)
    modify_orientation(Settings,settings_file)
    modify_default_amount_of_spectrums(Settings,settings_file)
    modify_default_mass_list(Settings,settings_file)
    modify_do_display_3d(Settings,settings_file)
    modify_do_display_const_mass(Settings,settings_file)
    modify_do_display_const_time(Settings,settings_file)

    reset_settings = st.button(label="reset all settings to default")
    if reset_settings:
        reset_to_default(settings_file,default_settings_file)







