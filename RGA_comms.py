import socket
import time
import datetime
import json
import sys
import pymodbus as pmb
from pymodbus.client import ModbusTcpClient
import JSONoperators as js
import AbnormalityReaction as ar



def SendPacketsToRGA(packages_list,ip_adress="169.254.198.174",show_live_feed=True):    #command to send multiple commands to RGA via list of strings
    HOST, PORT = ip_adress, 10014   #default IP and port of RGA, change later???

    data_list = list()

    for package in packages_list:
        data_list.append(bytes(package, "ascii")+bytes([10]))   #each string in packages_list is converted to bytes and appended to data_list

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:   # connection to RGA
        # Connect to server and send data
        sock.connect((HOST, PORT))
        placeholder = str(sock.recv(1024), "ascii")

        received_list = list()  # list for strings received from RGA

        for data in data_list:

            if "__listen__" in str(data,"ascii"):  # __listen__ command is intended to be executed by this computer, not by RGA



                data = str(data,"ascii")   # __listen__ n m waits for n amount of messages from RGA waiting m seconds between
                data_split = data.split()



                for i in range(int(data_split[1])):
                    received = str(sock.recv(1024), "ascii")

                    if "ERROR" in received:
                        sock.send(bytes("Release", "ascii") + bytes([10]))
                        raise ValueError("ERROR keyword in output")



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
                                    raise ValueError("ERROR keyword in output")


                                received_list.append(received)
                                received_split = received.split()

                                if "MassReading" in received_split:
                                    MassReadingPosition = received_split.index("MassReading")
                                    if float(received_split[MassReadingPosition+1]) >= float(data_split[1]):
                                        break



                                #if received_split[0] == "MassReading" and float(received_split[1]) >= float(data_split[1]):
                                    #break


            else:
                sock.send(data)
                #print(data)
                #time.sleep(3)
                received = str(sock.recv(1024), "ascii")

                if "ERROR" in received:
                    sock.send(bytes("Release", "ascii") + bytes([10]))
                    raise ValueError("ERROR keyword in output")


                if show_live_feed:
                    print(received)
                received_list.append(received)





        return(received_list)


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
    packages_list = ['Control  "MyProgram" "1.0"' , 'FilamentControl On']
    for i in range(int(amount_of_scans)):
        packages_list.append(f'AddSinglePeak SinglePeak{i} {start_mass+i*step} {accuracy} 0 0 0')
        packages_list.append(f'scanadd SinglePeak{i}')
    packages_list.append('ScanStart 1')
    packages_list.append(f'__wait_for_given_mass__ {start_mass+step*(amount_of_scans-1)}')
    packages_list.append( 'Release')




    RawInput = SendPacketsToRGA(packages_list,ip_adress)


    Spectrum = list()  # spectrum is a list of PPM's corresponding to integer molar masses
    for i in range(amount_of_scans):
        Spectrum.append(0)

    for line in RawInput:
        # print(line)
        split_line = line.split()
        if "MassReading" in line:
            #print(line)
            MassReadingPosition = split_line.index("MassReading")
            split_eng_notation = (split_line[MassReadingPosition+2]).split("e")  # output is given as engineering notation and need to be interpreted to readable form

            power = 10 ** (int(split_eng_notation[1]))

            end_result = (float(split_eng_notation[
                                    0]) * power) * convertion_coefficient  # convertion of engineering notation to readable form. Covertion cooficient is used for unit convertion

            Spectrum[ int((float(split_line[MassReadingPosition+1])-float(start_mass))/float(step)) ] = end_result
    return Spectrum




'''def AppendSpectrumJSON(filename,convertion_coefficient=1,accuracy=5,ip_adress="169.254.198.174"):  # function to get spectrum from spectrometer and append it to given JSON file

    handle = open(filename,"r")
    for line in handle:
        translated_line = json.loads(line)
        if translated_line["class"] == "metadata":
            start_mass, step, amount_of_scans = float(translated_line["initial_value"]), float(translated_line["step"]), int(translated_line["amount_of_scans"])
            break
    handle.close()

    Spectrum = GetMassSpectrum(convertion_coefficient,start_mass,amount_of_scans,step,accuracy,ip_adress)  # spectrum is obtained by making request to mass spectrometer


    handle = open(filename,"a")

    current_time = int(datetime.datetime.now().timestamp())
    line_to_append = {"class":"spectrum","time":current_time,"array":Spectrum}
    formatted_line = json.dumps(line_to_append)  # current time in computer format and array of PPM's are recorded into JSON formatted line

    handle.write("\n")
    handle.write(formatted_line)
    handle.close()'''


def AppendSpectrumJSON(filename,control_spectrum_filename,log_filename,convertion_coefficient=1,accuracy=5,ip_adress="169.254.198.174",doliveabnormalitycheck=False,do_emit_sound = True):  #scanning for great amount of values is memory complex, therefore multiple steps of scanning and writing is required

    handle = open(filename, "r")
    for line in handle:
        translated_line = json.loads(line)
        if translated_line["class"] == "metadata":
            start_mass, step, amount_of_scans = float(translated_line["initial_value"]), float(
                translated_line["step"]), int(translated_line["amount_of_scans"])
            break
    handle.close()



    current_time = int(datetime.datetime.now().timestamp())
    dictionary_to_append = {}
    dictionary_to_append["class"] = "spectrum"
    dictionary_to_append["time"] = current_time

    array_to_append = []




    while amount_of_scans > 0:

        if amount_of_scans > 128:
            temp_amount_of_scans = 128
            amount_of_scans = amount_of_scans - 128
        else:
            temp_amount_of_scans = amount_of_scans
            amount_of_scans = 0


        Spectrum = GetMassSpectrum(convertion_coefficient, start_mass, temp_amount_of_scans, step, accuracy, ip_adress)
        for element in Spectrum:
                array_to_append.append(element)

        start_mass = start_mass + 128*step




    if doliveabnormalitycheck:

        controlspectrum_handle = open(control_spectrum_filename, "r")  #required data loaded from control spectrum
        for line in controlspectrum_handle:
            match json.loads(line)["class"]:
                case "control_spectrum":
                    controlspectrum = json.loads(line)
                case "metadata":
                    control_metadata = json.loads(line)
        controlspectrum_handle.close()

        ar.FindAbnormalityInSpectrum(array_to_append,controlspectrum,current_time,True,filename,log_filename,start_mass,step,do_emit_sound=False,simplex=True)



    dictionary_to_append["array"] = array_to_append

    handle = open(filename, "a")
    handle.write("\n")
    handle.write(json.dumps(dictionary_to_append))
    handle.close()



def OpenMassFlowController():

    client = ModbusTcpClient('',502)
    client.connect()

    client.write_coil(1, True)
    result = client.read_coils(1,1)
    result2 = client.readwrite_registers(read_adress="0x00")
    print(result.bits[0])
    print(result2)
    client.close()



#AppendGreatSpectrumJSON('FullScan',1,5,"169.254.198.174")

#Output = SendPacketsToRGA( ('Control  "MyProgram" "1.0"','FilamentControl On','AddSinglePeak Peak1 37.5 5 0 0 0','scanadd Peak1','ScanStart 1','__listen__ 20 0','Release') )
#Output = SendPacketsToRGA( ('Control  "MyProgram" "1.0"', 'FilamentControl On', 'AddSinglePeak SinglePeak0 39.0 5 0 0 0', 'scanadd SinglePeak0', 'ScanStart 1', '__wait_for_given_mass__ 39.0', 'Release'))


#Output = SendPacketsToRGA( ('Control  "MyProgram" "1.0"','FilamentControl On','AddBarchart Bar1 1 100 PeakCenter 5 0 0 0','scanadd Bar1','ScanStart 1','__listen__ 100 0','Release') )
#Output = SendPacketsToRGA( ('Control  "MyProgram" "1.0"','FilamentControl On','AddBarchart Bar1 1 100 PeakCenter 5 0 0 0','scanadd Analog1','ScanStart 1','__listen__ 100 0','Release') )

#for element in Output:
 #   print(element)

#TestSpectrum = GetMassSpectrum(1)
#print(TestSpectrum)

