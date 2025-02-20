from subprocess import STDOUT

import streamlit as st
import json
import datetime
import os
import JSONoperators as js
import SimpleXChat_Interface as sxci
import Logging
import subprocess





# function to analyse JSON spectrum file for abnormalities and print results to log file
def AnalyseFile(spectrum_filename,MainConfig="MainConfig"):
    handle = open(spectrum_filename, "r")
    abnormalities_detected_in_file = False
    all_log_entries = []

    for line in handle:
        if line == "" or line == "\n" or line[0] == "#":
            continue
        # print(line)
        tempdict = json.loads(line)
        match tempdict["class"]:
            case "metadata":
                metadata = tempdict
                assert metadata["is_a_spectrum"] == "True"
            case "spectrum":
                pass

    handle.close()
    handle = open(spectrum_filename, "r")


    for line in handle:
        if line == "" or line == "\n" or line[0] == "#":
            continue
        # print(line)
        tempdict = json.loads(line)
        match tempdict["class"]:
            case "metadata":
                pass
            case "spectrum":
                abnormalities_detected,log_entries = AnalyseSingleLine(tempdict,metadata["valve_number"],metadata["initial_value"],metadata["step"],spectrum_filename,DoLogging=False)
                if abnormalities_detected:
                    abnormalities_detected_in_file = True
                    for element in log_entries:
                        all_log_entries.append(element)

    handle.close()
    return abnormalities_detected_in_file,all_log_entries



# Function to analyse single spectrum for abnormalities
def AnalyseSingleLine(spectrum_to_analyze,multi_inlet_valve, initial_mass, step, filename, DoLogging=True):



    i = 0
    sound_already_emitted = False

    abnormalities_detected = False
    log_entries = []

    pascal_spectrum = spectrum_to_analyze["array"]
    spectrum = []

    control_spectrum = js.ReadJSONConfig("AbnormalityReaction",f"MIV{multi_inlet_valve}")

    pascal_sum = 0
    for element in pascal_spectrum:
        pascal_sum = pascal_sum + abs(element)
    for element in pascal_spectrum:
        spectrum.append((abs(element) * 1000000) / pascal_sum)


    try:
        oxygen = spectrum_to_analyze["oxygen"]
    except:
        oxygen = 0

    for element in spectrum:
        if int(initial_mass + step*i) == float(initial_mass + step*i):  # only integer peaks are analysed


            try:  # if boundaries for specific mass are specified, those boundaries are used for comparison
                boundaries = control_spectrum[str(f'{int(initial_mass + step * i)}')]
            except:  # else, boundaries are set to default
                boundaries = control_spectrum["default"]



            if element > float(boundaries[1]) or element < float(boundaries[0]):  # if element is smaller than minimal accepted or greater that maximal accepted:
                    abnormalities_detected = True
                    log_entry = f"Valve position {multi_inlet_valve}, Filename {filename}: PPM for M/Z = {int(initial_mass + step * i)} is {element}, while boundaries are {boundaries[0]}:{boundaries[1]}"
                    if DoLogging:
                        Logging.MakeLogEntry(log_entry,log_name="AbnormalityLog")

                        try:
                            ret = str((subprocess.run(["pwd"], capture_output=True)).stdout)

                            ret = ret.strip("b")
                            ret = ret.strip("'")
                            ret = ret.strip("\\n")

                            os.system(f'notify-send -u critical -i {ret}/AbnormalityIcon.png "{log_entry}"')
                        except:

                            os.system(f'notify-send -u critical "{log_entry}"')

                        

                    log_entries.append(log_entry)




        i += 1



    oxygen_boundaries = control_spectrum[str(f'oxygen')]
    if oxygen > float(oxygen_boundaries[1]) or oxygen < float(oxygen_boundaries[0]):
        abnormalities_detected = True
        log_entry = f"Valve position {multi_inlet_valve}, Filename {filename}: PPM for oxygen is {oxygen}, while boundaries are {oxygen_boundaries[0]}:{oxygen_boundaries[1]}"
        if DoLogging:
            Logging.MakeLogEntry(log_entry, log_name="AbnormalityLog")
        log_entries.append(log_entry)


    return abnormalities_detected, log_entries




#def MakeLogEntry()







#AnalyseSpectrum("FullScan","ControlSpectrumTest","AbnormalityLog",True)