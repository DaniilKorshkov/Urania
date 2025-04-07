import socket
import time
import datetime
import json

from pyarrow import timestamp

import JSONoperators as js
import AbnormalityReaction as ar
import Logging
import os
import SimpleXChat_Interface as sxci
import netdiscover
import oxygen_analyzer as oxa
from JSONoperators import ReadJSONConfig
import datetime


def SendPacketsToRGA(packages_list,ip_adress="169.254.198.174",show_live_feed=True):    #command to send multiple commands to RGA via list of strings

    ip_adress = js.ReadJSONConfig("spectrometer_parameters","ip_address")
    timeout_time = js.ReadJSONConfig("spectrometer_parameters","timeout_time")
    initial_time = (datetime.datetime.now()).timestamp()

    HOST, PORT = ip_adress, 10014   #default IP and port of RGA, change later???
    ErrorMessage = None

    data_list = list()

    for package in packages_list:
        data_list.append(bytes(package, "ascii")+bytes([10]))   #each string in packages_list is converted to bytes and appended to data_list

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:   # connection to RGA
        # Connect to server and send data
        sock.connect((HOST, PORT))
        placeholder = str(sock.recv(1024), "ascii")

        received_list = list()  # list for strings received from RGA

        for data in data_list:

            if ErrorMessage == None:

                if "__listen__" in str(data,"ascii"):  # __listen__ command is intended to be executed by this computer, not by RGA



                    data = str(data,"ascii")   # __listen__ n m waits for n amount of messages from RGA waiting m seconds between
                    data_split = data.split()



                    for i in range(int(data_split[1])):
                        received = str(sock.recv(1024), "ascii")

                        if "ERROR" in received:
                            sock.send(bytes("Release", "ascii") + bytes([10]))
                            ErrorMessage = received
                            return None, ErrorMessage
                            #raise ValueError("ERROR keyword in output")



                        #print(received)
                        received_list.append(received)
                        time.sleep(int(data_split[2]))

                elif "__wait_for_given_mass__" in str(data,"ascii"):  #command to keep listening on port until desired mass appears (for ex., __wait_for_given_mass__ 100)

                                data = str(data, "ascii")  # __listen__ n m waits for n amount of messages from RGA waiting m seconds between
                                data_split = data.split(" ")
                                while True:
                                    if show_live_feed:
                                        print(received)
                                    received = str(sock.recv(1024), "ascii")

                                    if "ERROR" in received:
                                        sock.send(bytes("Release", "ascii") + bytes([10]))
                                        ErrorMessage = received

                                        return None, ErrorMessage


                                    received_list.append(received)
                                    received_split = received.split()

                                    if "MassReading" in received_split:
                                        MassReadingPosition = received_split.index("MassReading")
                                        if float(received_split[MassReadingPosition+1]) >= float(data_split[1]):
                                            break

                                    if (datetime.datetime.now()).timestamp() > initial_time + timeout_time:
                                        ErrorMessage = "TIMEOUT"

                                        return None, ErrorMessage




                                    #if received_split[0] == "MassReading" and float(received_split[1]) >= float(data_split[1]):
                                        #break

                elif "Release" in str(data, "ascii"):
                    while True:
                        sock.send(bytes("Release", "ascii") + bytes([10]))
                        received = str(sock.recv(1024), "ascii")
                        if ("Release OK" or "Must be in control of sensor to release control") in received:
                            break
                        else:
                            continue





                else:
                    sock.send(data)
                    #print(data)
                    #time.sleep(3)
                    received = str(sock.recv(1024), "ascii")

                    if "ERROR" in received:

                        while True:
                            sock.send(bytes("Release", "ascii") + bytes([10]))
                            received = str(sock.recv(1024), "ascii")
                            if ("Release OK" or "Must be in control of sensor to release control") in received:
                                break
                            else:
                                continue




                        ErrorMessage = received
                        print(ErrorMessage)
                        return None, ErrorMessage


                    if show_live_feed:
                        print(received)
                    received_list.append(received)





        return received_list, ErrorMessage


'''def GetMassSpectrum(convertion_coefficient=1,amount_of_scans=100,ip_adress="169.254.198.174"):
    RawInput = SendPacketsToRGA(('Control  "MyProgram" "1.0"','FilamentControl On',f'AddBarchart Bar1 1 {amount_of_scans} PeakCenter 5 0 0 0','scanadd Bar1','ScanStart 1',f'__wait_for_given_mass__ {amount_of_scans} 0','Release'),ip_adress)
    Spectrum = list()  # spectrum is a list of PPM's corresponding to integer molar masses

    for i in range(amount_of_scans):
        Spectrum.append(0)

    prev_mass = 0
    for line in RawInput:
        split_line = line.split()

        if "MassReading" in line:


            MassReadingPosition = split_line.index("MassReading") # in rare cases mass reading os not the zeroth element in list. Finding position of "MassReading" in line is a workaround

            split_eng_notation = (split_line[MassReadingPosition+2]).split("e")  #output is given as engineering notation and need to be interpreted to readable form


            power = 10**(int(split_eng_notation[1]))


            end_result = (float(split_eng_notation[0])*power)*convertion_coefficient  # convertion of engineering notation to readable form. Covertion cooficient is used for unit convertion

            Spectrum[split_line[MassReadingPosition+1]] = end_result
    return Spectrum



def AppendSpectrumJSON(filename,convertion_coefficient,ip_adress="169.254.198.174"):  # function to get spectrum from spectrometer and append it to given JSON file
    Spectrum = GetMassSpectrum(convertion_coefficient,ip_adress)  # spectrum is obtained by making request to mass spectrometer

    handle = open(filename,"a")

    current_time = int(datetime.datetime.now().timestamp())
    line_to_append = {"class":"spectrum","time":current_time,"array":Spectrum}
    formatted_line = json.dumps(line_to_append)  # current time in computer format and array of PPM's are recorded into JSON formatted line

    handle.write("\n")
    handle.write(formatted_line)
    handle.close()'''



def GetMassSpectrum(convertion_coefficient,start_mass,amount_of_scans,step=1,accuracy=5,ip_adress="169.254.198.174"):

    MaxMultiplierIntensity = ReadJSONConfig("spectrometer_parameters","MaxMultiplierIntensity")
    MultiplierMode = 0
    #MultiplierMode = js.ReadJSONConfig("spectrometer_parameters","MultiplierMode")
    #assert MultiplierMode in range(4)
    packages_list = ['Control  "MyProgram" "1.0"' , 'FilamentControl On']
    for i in range(int(amount_of_scans)):

        timestamp = int(1000000*(datetime.datetime.now()).timestamp())
        packages_list.append(f'AddSinglePeak {timestamp}RSP{i} {start_mass+i*step} {2} 0 0 0')
        packages_list.append(f'scanadd {timestamp}RSP{i}')
    packages_list.append(f"MeasurementDetectorIndex {0}")
    packages_list.append('ScanStart 1')
    packages_list.append(f'__wait_for_given_mass__ {start_mass+step*(amount_of_scans-1)}')
    packages_list.append( 'Release')




    RawInput, ErrorMessage = SendPacketsToRGA(packages_list,ip_adress)

    if ErrorMessage != None:
        return None, ErrorMessage


    ReconSpectrum = list()  # spectrum is a list of PPM's corresponding to integer molar masses
    for i in range(amount_of_scans):
        ReconSpectrum.append(0)

    for line in RawInput:
        # print(line)
        split_line = line.split()
        if "MassReading" in line:
            #print(line)
            MassReadingPosition = split_line.index("MassReading")
            split_eng_notation = (split_line[MassReadingPosition+2]).split("e")  # output is given as engineering notation and need to be interpreted to readable form

            power = 10 ** (int(split_eng_notation[1]))

            end_result = (float(split_eng_notation[0]) * power) * convertion_coefficient  # convertion of engineering notation to readable form. Covertion cooficient is used for unit convertion

            ReconSpectrum[ int((float(split_line[MassReadingPosition+1])-float(start_mass))/float(step)) ] = end_result

    FaradayCupMasses = list()
    MultiplierMasses = list()

    Spectrum = list()
    for i in range(amount_of_scans):
        Spectrum.append(0)

    i = 0
    for element in ReconSpectrum:
        if element > MaxMultiplierIntensity:
            FaradayCupMasses.append(start_mass+i*step)
        else:
            MultiplierMasses.append(start_mass+i*step)

        i += 1




    packages_list = ['Control  "MyProgram" "2.0"', 'FilamentControl On']
    j = amount_of_scans
    for MolarMass in FaradayCupMasses:
        timestamp = int(1000000*(datetime.datetime.now()).timestamp())
        packages_list.append(f'AddSinglePeak {timestamp}FSP{j} {MolarMass} {accuracy} 0 0 0')
        packages_list.append(f'scanadd {timestamp}FSP{j}')
        j += 1
    packages_list.append(f"MeasurementDetectorIndex {0}")
    packages_list.append('ScanStart 1')
    packages_list.append(f'__wait_for_given_mass__ {FaradayCupMasses[(len(FaradayCupMasses)-1)]}')
    packages_list.append('Release')

    RawInput, ErrorMessage = SendPacketsToRGA(packages_list, ip_adress)
    if ErrorMessage != None:
        return None, ErrorMessage

    for line in RawInput:
        # print(line)
        split_line = line.split()
        if "MassReading" in line:
            #print(line)
            MassReadingPosition = split_line.index("MassReading")
            split_eng_notation = (split_line[MassReadingPosition+2]).split("e")  # output is given as engineering notation and need to be interpreted to readable form

            power = 10 ** (int(split_eng_notation[1]))

            end_result = (float(split_eng_notation[0]) * power) * convertion_coefficient  # convertion of engineering notation to readable form. Covertion cooficient is used for unit convertion

            Spectrum[ int((float(split_line[MassReadingPosition+1])-float(start_mass))/float(step)) ] = end_result


    packages_list = ['Control  "MyProgram" "3.0"', 'FilamentControl On']

    for MolarMass in MultiplierMasses:
        timestamp = int(1000000*(datetime.datetime.now()).timestamp())
        packages_list.append(f'AddSinglePeak {timestamp}MSP{j} {MolarMass} {accuracy} 0 0 0')
        packages_list.append(f'scanadd {timestamp}MSP{j}')
        j += 1
    packages_list.append(f"MeasurementDetectorIndex {1}")
    packages_list.append('ScanStart 1')
    packages_list.append(f'__wait_for_given_mass__ {MultiplierMasses[(len(MultiplierMasses)-1)]}')
    packages_list.append('Release')

    RawInput, ErrorMessage = SendPacketsToRGA(packages_list, ip_adress)
    if ErrorMessage != None:
        return None, ErrorMessage

    for line in RawInput:
        # print(line)
        split_line = line.split()
        if "MassReading" in line:
            # print(line)
            MassReadingPosition = split_line.index("MassReading")
            split_eng_notation = (split_line[MassReadingPosition + 2]).split(
                "e")  # output is given as engineering notation and need to be interpreted to readable form

            power = 10 ** (int(split_eng_notation[1]))

            end_result = (float(split_eng_notation[
                                    0]) * power) * convertion_coefficient  # convertion of engineering notation to readable form. Covertion cooficient is used for unit convertion

            Spectrum[int((float(split_line[MassReadingPosition + 1]) - float(start_mass)) / float(step))] = end_result







    return Spectrum, ErrorMessage





def AppendSpectrumJSON(filename,convertion_coefficient=1,accuracy=5,config="MainConfig"):  #scanning for great amount of values is memory complex, therefore multiple steps of scanning and writing is required



    ip_adress = js.ReadJSONConfig("spectrometer_parameters","ip_address",config)


    handle = open(filename, "r")
    for line in handle:
        translated_line = json.loads(line)
        if translated_line["class"] == "metadata":
            start_mass, step, amount_of_scans = float(translated_line["initial_value"]), float(
                translated_line["step"]), int(translated_line["amount_of_scans"])
            break
    handle.close()

    real_start_mass = start_mass

    current_time = int(datetime.datetime.now().timestamp())
    dictionary_to_append = {}
    dictionary_to_append["class"] = "spectrum"
    dictionary_to_append["time"] = current_time

    array_to_append = []

    ErrorMessage = None

    Logging.MakeLogEntry(f"RGA scan for Filename = {filename}, Minit = {real_start_mass}, step={step}, amt.of steps = {amount_of_scans} initiated")




    while amount_of_scans > 0 and ErrorMessage == None:

        if amount_of_scans > 128:
            temp_amount_of_scans = 128
            amount_of_scans = amount_of_scans - 128
        else:
            temp_amount_of_scans = amount_of_scans
            amount_of_scans = 0


        Spectrum, ErrorMessage = GetMassSpectrum(convertion_coefficient, start_mass, temp_amount_of_scans, step, accuracy, ip_adress)

        if ErrorMessage != None:
            break

        for element in Spectrum:
                array_to_append.append(element)

        start_mass = start_mass + 128*step





    if ErrorMessage == None:

        dictionary_to_append["array"] = array_to_append
        try:
            dictionary_to_append["oxygen"] = oxa.GetOxygenData("MainConfig")
            Logging.MakeLogEntry(f"Received oxygen data for RGA scan: {filename}")
        except:
            Logging.MakeLogEntry(f"Failed to get oxygen data for RGA scan: {filename}")
            dictionary_to_append["oxygen"] = 0


        handle = open(filename, "a")
        handle.write("\n")
        handle.write(json.dumps(dictionary_to_append))
        handle.close()
        Logging.MakeLogEntry(f"RGA scan for Filename = {filename}, Minit = {real_start_mass}, step={step}, amt.of steps = {amount_of_scans} completed without errors")

    else:
        Logging.MakeLogEntry(f"Following error was encountered during RGA scan: {ErrorMessage}")
        Logging.MakeLogEntry(f"RGA scan for Filename = {filename}, Minit = {real_start_mass}, step={step}, amt.of steps = {amount_of_scans} completed with error")
        if ErrorMessage == "TIMEOUT":
            change_rga_ip()

        return None, None, None, ErrorMessage



    return dictionary_to_append, real_start_mass, step, ErrorMessage









def control_pump(status,MainConfig="MainConfig"):
    match status.lower():
        case "on":
            SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,"CirrusPump True", "Release"])
        case "off":
            SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,"CirrusPump False", "Release"])



def control_heater(status,MainConfig="MainConfig"):
    match status.lower():
        case "off":
            SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,"CirrusHeater Off", "Release"])
        case "warm":
            SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,"CirrusHeater Warm", "Release"])
        case "bake":
            SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,"CirrusHeater Bake", "Release"])


def control_capillary_heater(status,MainConfig="MainConfig"):
    match status.lower():
        case "on":
            SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,"CirrusCapillaryHeater True", "Release"])
        case "off":
            SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,"CirrusCapillaryHeater False", "Release"])



def heating_info(MainConfig="MainConfig"):

    ret,void = SendPacketsToRGA(["CirrusInfo"])
    splitret = ret[0].split("\n")
    print("ret="+splitret[0])

    heatstat = None
    pumpstat = None
    capheatstat = None

    for element in splitret:
        elementsplit = element.split()



        if "HeaterStatus" in elementsplit:

            position = elementsplit.index("HeaterStatus")

            heatstat = elementsplit[position+1]

        if "CapillaryHeaterStatus" in elementsplit:

            position = elementsplit.index("CapillaryHeaterStatus")
            capheatstat = elementsplit[position + 1]
        if "PumpStatus" in elementsplit:

            position = elementsplit.index("PumpStatus")
            pumpstat = elementsplit[position + 1]


    return heatstat, capheatstat, pumpstat



def rga_filament_info(MainConfig="MainConfig"):
    ret, void = SendPacketsToRGA(["FilamentInfo"])
    splitret = ret[0].split("\n")
    print("ret=" + splitret[0])

    filamentstatus = None
    activefilament = None

    for element in splitret:
        elementsplit = element.split()

        if "SummaryState" in elementsplit:

            position = elementsplit.index("SummaryState")

            filamentstatus = elementsplit[position+1]

        if "ActiveFilament" in elementsplit:
            position = elementsplit.index("ActiveFilament")

            activefilament = elementsplit[position + 1]




    return filamentstatus, activefilament



def rga_filament_select(value, MainConfig="MainConfig"):
    SendPacketsToRGA(['Control  "MyProgram" "1.0"' , f"FilamentSelect {value}", "Release"])


def rga_filament_control(status, MainConfig = "MainConfig"):
    SendPacketsToRGA(['Control  "MyProgram" "1.0"' ,f"FilamentControl {status}","Release"])


def rga_multiplier_info(MainConfig="MainConfig"):
    ret, void = SendPacketsToRGA(["MultiplierInfo"])
    splitret = ret[0].split("\n")
    print("ret=" + splitret[0])

    multiplier_status = None


    for element in splitret:
        elementsplit = element.split()

        if "MultiplierOn" in elementsplit:
            position = elementsplit.index("MultiplierOn")

            multiplier_status = elementsplit[position + 1]

            break



    return multiplier_status



def rga_multiplier_status(MainConfig="MainConfig"):
    ret, void = SendPacketsToRGA(["MultiplierInfo"])
    splitret = ret[0].split("\n")
    print("ret=" + splitret[0])

    multiplier_status = None

    for element in splitret:
        elementsplit = element.split()

        if "MultiplierOn" in elementsplit:
            position = elementsplit.index("MultiplierOn")

            multiplier_status = elementsplit[position + 1]

            break

    return multiplier_status


'''def rga_detector_type(MainConfig="MainConfig"):
    ret, void = SendPacketsToRGA(["Info"])
    splitret = ret[0].split("\n")
    print("ret=" + splitret[0])

    multiplier_status = None

    for element in splitret:
        elementsplit = element.split()

        if "MultiplierOn" in elementsplit:
            position = elementsplit.index("MultiplierOn")

            multiplier_status = elementsplit[position + 1]

            break

    return multiplier_status'''



def change_rga_ip(MainConfig="MainConfig"):
    disc = netdiscover.Discover()
    mac = js.ReadJSONConfig("spectrometer_parameters","mac_address")
    ret = js.ReadJSONConfig("spectrometer_parameters","ip_address")
    scan = disc.scan(ip_range="192.168.0.0/24")
    if_success = False
    for element in scan:
        if element["mac"] == mac:
            ret = element["ip"]
            if_success = True

    handle = open("MainConfig","r")
    newconfig = []
    for line in handle:
                try:
                    dictline = json.loads(line)
                    if dictline["class"] == "spectrometer_parameters":
                        dictline["ip_address"] = ret
                        newline = json.dumps(dictline)
                        newconfig.append(newline+"\n")
                    else:
                        newconfig.append(line)
                except:
                    pass
    handle.close()

    handle = open("MainConfig","w")
    for line in newconfig:
                handle.write(line)
    handle.close()

    return if_success, ret





