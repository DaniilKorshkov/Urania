import streamlit as st
import json
import datetime
import os
import JSONoperators as js
import SimpleXChat_Interface as sxci
import Logging



# function to analyse JSON spectrum file for abnormalities and print results to log file
'''def AnalyseSpectrum(spectrum_filename,control_spectrum_filename,log_filename,do_report_to_log):
    controlspectrum_handle = open(control_spectrum_filename, "r")
    for line in controlspectrum_handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        match json.loads(line)["class"]:
            case "control_spectrum":
                controlspectrum = json.loads(line)
            case "metadata":
                control_metadata = json.loads(line)
    controlspectrum_handle.close()

    spectrum_metadata, spectrum_list, oxygen_list = js.read_spectrum_json(spectrum_filename)

    for time_key in spectrum_list:
        FindAbnormalityInSpectrum(spectrum_list[time_key], controlspectrum, time_key,
                                  do_report_to_log, spectrum_filename, log_filename, spectrum_metadata["initial_value"],
                                  spectrum_metadata["step"])


    spectrum_handle = open(spectrum_filename,"r")

    for line in spectrum_handle:
        match json.loads(line)["class"]:
            case "metadata":
                spectrum_metadata = json.loads(line)
            case "spectrum":'''



# Function to analyse single spectrum for abnormalities
def AnalyseSingleLine(spectrum_to_analyze,multi_inlet_valve, initial_mass, step, filename):



    i = 0
    sound_already_emitted = False

    abnormalities_detected = False

    pascal_spectrum = spectrum_to_analyze["array"]
    spectrum = []

    control_spectrum = js.ReadJSONConfig("AbnormalityReaction",f"MIV{multi_inlet_valve}")

    pascal_sum = 0
    for element in pascal_spectrum:
        pascal_sum = pascal_sum + abs(element)
    for element in pascal_spectrum:
        spectrum.append((abs(element) * 1000000) / pascal_sum)



    oxygen = spectrum_to_analyze["oxygen"]

    for element in spectrum:
        if int(initial_mass + step*i) == float(initial_mass + step*i):  # only integer peaks are analysed


            try:  # if boundaries for specific mass are specified, those boundaries are used for comparison
                boundaries = control_spectrum[str(f'{int(initial_mass + step * i)}')]
            except:  # else, boundaries are set to default
                boundaries = control_spectrum["default"]



            if element > boundaries[1] or element < boundaries[0]:  # if element is smaller than minimal accepted or greater that maximal accepted:
                abnormalities_detected = True
                Logging.MakeLogEntry(f"Valve position {multi_inlet_valve}, Filename {filename}: PPM for M/Z = {int(initial_mass + step * i)} is {element}, while boundaries are {boundaries[0]}:{boundaries[1]}",log_name="AbnormalityLog")




        i += 1
    oxygen_boundaries = control_spectrum[str(f'oxygen')]
    if oxygen > oxygen_boundaries[1] or oxygen < oxygen_boundaries[0]:
        abnormalities_detected = True
        Logging.MakeLogEntry(f"Valve position {multi_inlet_valve}, Filename {filename}: PPM for oxygen is {oxygen}, while boundaries are {oxygen_boundaries[0]}:{oxygen_boundaries[1]}", log_name="AbnormalityLog")


    return abnormalities_detected




#def MakeLogEntry()







#AnalyseSpectrum("FullScan","ControlSpectrumTest","AbnormalityLog",True)