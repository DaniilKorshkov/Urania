import json
import Functions as fn
import os
import streamlit as st

'''def file_selector(folder_path='.'):
    filename = st.file_uploader(label="Select a spectrum file", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None,
                     kwargs=None, disabled=False)
    return filename'''


def read_spectrum_json(filename):   #function to read array of spectrums from JSON files

    metadata = {}
    spectrum_list = {}            #array of spectrums is presented as dictionaty with time used as key and list of PPM's for each mass used as respective value
    oxygen_list = {}

    handle = open(filename, "r")

    for line in handle:
        if line == "" or line == "\n" or line[0] == "#":
            continue
        #print(line)
        tempdict = json.loads(line)
        match tempdict["class"]:
            case "metadata":
                metadata = tempdict
                assert metadata["is_a_spectrum"] == "True"
            case "spectrum":
                time = tempdict["time"]
                spectrum_array = tempdict["array"]
                try:
                    oxygen = tempdict["oxygen"]
                except:
                    oxygen = 0

                spectrum_list[str(time)] = spectrum_array
                oxygen_list[str(time)] = oxygen

    handle.close()
    return metadata, spectrum_list, oxygen_list



def read_last_spectrums(filename, howmuchspectrums):   # function to get X most recent spectrums from full array


    metadata, spectrum_list, oxygen_list = read_spectrum_json(filename)
    time_list = fn.get_time_list(spectrum_list)  # list of all time moments of spectrums in full array of spectrums
    lng = len(spectrum_list)
    time_list.sort()


    if howmuchspectrums > lng:
        howmuchspectrums = lng


    new_spectrum_list = {}
    new_oxygen_list = {} # only spectrums corresponding to X latest moments of time are appended to new_spectrum_list
    for i in range(howmuchspectrums):
        new_spectrum_list[str(time_list[lng-i-1])] = spectrum_list[str(time_list[lng-i-1])]
        new_oxygen_list[str(time_list[lng-i-1])] = oxygen_list[str(time_list[lng-i-1])]

    return metadata, new_spectrum_list, new_oxygen_list      #new_spectrum_list is returned


def read_GUI_page_settings(filename, self_name):   #function to read settings for given page for GUI from JSON format

    GUI_page_settings = {}

    handle = open(filename, "r")

    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        try:
            tempdict = json.loads(line)
            if tempdict["page_name"] == self_name:  #if page_name in JSON config equals the desired name, settings are returned
                GUI_page_settings = tempdict
        except:
            pass

    handle.close()
    return GUI_page_settings


def read_period_of_time(filename, howmuchspectrums, desired_time):  #function to read X spectrums starting from given moment of time

    metadata, spectrum_list, oxygen_list = read_spectrum_json(filename)
    time_list = fn.get_time_list(spectrum_list)  # list of all time moments of spectrums in full array of spectrums


    lng = len(spectrum_list)
    time_list.sort()

    t = 0  # counter for finding desired time

    time_found = False #error handler if desired time is bigger than last measurement

    for element in time_list:
        if element >= desired_time: #ineffective search algorithm, fix later?
            time_found = True # finding closest match to desired time
            break
        else:
            t += 1


    if time_found:
        new_spectrum_list = {}
        new_oxygen_list = {} # only spectrums corresponding to desired time boundaries are added to new_spectrum_list
        for i in range(howmuchspectrums):
                try:
                    new_spectrum_list[str(time_list[t+i])] = spectrum_list[str(time_list[t+i])]
                    new_oxygen_list[str(time_list[t + i])] = oxygen_list[str(time_list[t + i])]

                except:
                    pass
    else: # in desired time is bigger than most recent spectrum, only single last spectrum is added to new_spectrum_list
        new_spectrum_list = {}
        new_oxygen_list = {}
        new_spectrum_list[str(time_list[t-1])] = spectrum_list[str(time_list[t-1])]
        new_oxygen_list[str(time_list[t - 1])] = oxygen_list[str(time_list[t - 1])]


    return metadata, new_spectrum_list, new_oxygen_list





def read_all_page_numbers(filename):   # function to read all page numbers from JSON config

    page_numbers = []

    handle = open(filename, "r")

    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        tempdict = json.loads(line)
        page_numbers.append(tempdict["page_name"])

    handle.close()

    return page_numbers


def assert_file_exists(filename,default_image_filename=None):
    try:
        handle = open(filename,"r")
        handle.close()
    except:
        os.system(f"touch {filename}")

        if default_image_filename != None:

            handle = open(default_image_filename,"r")
            copy = []
            for line in handle:
                copy.append(line)
            handle.close()

            handle = open(filename,"w")
            for line in copy:
                handle.write(line)
            handle.close()


def ReadJSONConfig(linename,entryname,config="MainConfig"): #function to read a specific entry from specified line in config
    handle = open(config, "r")
    for line in handle:

        if line == "" or line == "\n" or line[0] == "#" or line == None:
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == linename:
            entry = dict_line[entryname]
            break
    handle.close()

    if entry == None:
        raise LookupError(f"{entryname} entry was not found in {linename} line in {config} config")

    return entry
