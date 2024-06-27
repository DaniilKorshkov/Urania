import streamlit as st
import json
import datetime
import os
import JSONoperators as js
import SimpleXChat_Interface as sxci



# function to analyse JSON spectrum file for abnormalities and print results to log file
def AnalyseSpectrum(spectrum_filename,control_spectrum_filename,log_filename,do_report_to_log):
    controlspectrum_handle = open(control_spectrum_filename, "r")
    for line in controlspectrum_handle:
        match json.loads(line)["class"]:
            case "control_spectrum":
                controlspectrum = json.loads(line)
            case "metadata":
                control_metadata = json.loads(line)
    controlspectrum_handle.close()

    spectrum_metadata, spectrum_list = js.read_spectrum_json(spectrum_filename)

    for time_key in spectrum_list:
        FindAbnormalityInSpectrum(spectrum_list[time_key], controlspectrum, time_key,
                                  do_report_to_log, spectrum_filename, log_filename, spectrum_metadata["initial_value"],
                                  spectrum_metadata["step"])


    '''spectrum_handle = open(spectrum_filename,"r")

    for line in spectrum_handle:
        match json.loads(line)["class"]:
            case "metadata":
                spectrum_metadata = json.loads(line)
            case "spectrum":'''



# Function to analyse single spectrum for abnormalities
def FindAbnormalityInSpectrum(spectrum,controlspectrum,measurement_time,do_report_to_json,spectrum_filename,log_filename,initial_mass=1,step=1,emitsound=False,simplex=True):
    i = 0
    sound_already_emitted = False

    for element in spectrum:
        if int(initial_mass + step*i) == float(initial_mass + step*i):  # only integer peaks are analysed


            try:  # if boundaries for specific mass are specified, those boundaries are used for comparison
                boundaries = controlspectrum[str(f'{int(initial_mass + step * i)}')]
            except:  # else, boundaries are set to default
                boundaries = controlspectrum["default_boundaries"]



            if element > boundaries[1] or element < boundaries[0]:  # if element is smaller than minimal accepted or greater that maximal accepted:

                    if emitsound and (not sound_already_emitted):  # sound notification
                        for i in range(3):
                            os.system('play -nq -t alsa synth {} sine {}'.format(0.1, 440))
                        sound_already_emitted = True

                    if simplex:
                        ReportAbnormalityViaSimpleXChat(spectrum_filename, measurement_time, (initial_mass + step*i), element,boundaries)




                    if do_report_to_json:  # scenario 1 - abnormality logged to JSON file

                        ReportAbnormalityToTextFile(log_filename,spectrum_filename,measurement_time,(initial_mass + step*i),element,boundaries)



                    else:  # scenario 2 - abnormality messages are displayed live
                        try:
                            boundaries = controlspectrum[str(int(initial_mass + step * i))]
                        except:
                            boundaries = controlspectrum['default_boundaries']

                        st.write(f'{datetime.datetime.fromtimestamp(int(measurement_time))}: PP(M???) for M={initial_mass + step * i} is {element} while tolerable interval is {boundaries}')

        i += 1




def ReportAbnormalityViaSimpleXChat(spectrum_filename,measurement_time,molar_mass,abnormal_value,boundaries):
    message = f'{datetime.datetime.fromtimestamp(int(measurement_time))}, filename - {spectrum_filename}: Molar mass at peak {molar_mass} is {abnormal_value}, while boundaries are {boundaries}'
    #message = 'error'
    sxci.SendCommandToUser(message)





# function to append single line into abnormality log
def ReportAbnormalityToTextFile(log_filename,spectrum_filename,measurement_time,molar_mass,abnormal_value,boundaries):
    handle = open(log_filename, "a")

    handle.write(f'\n{datetime.datetime.fromtimestamp(int(measurement_time))}, filename - {spectrum_filename}: Molar mass at peak {molar_mass} is {abnormal_value}, while boundaries are {boundaries}')
    handle.close()


#AnalyseSpectrum("FullScan","ControlSpectrumTest","AbnormalityLog",True)