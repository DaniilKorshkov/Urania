import socket
import time
import datetime
import json
import sys
#import pymodbus as pmb
#from pymodbus.client import ModbusTcpClient



def SendPacketsToRGA(packages_list,ip_adress="169.254.198.174"):    #command to send multiple commands to RGA via list of strings
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
                    #print(received)
                    received_list.append(received)
                    time.sleep(int(data_split[2]))

            elif "__wait_for_given_mass__" in str(data,"ascii"):  #command to keep listening on port until desired mass appears (for ex., __wait_for_given_mass__ 100)

                            data = str(data, "ascii")  # __listen__ n m waits for n amount of messages from RGA waiting m seconds between
                            data_split = data.split(" ")
                            while True:
                                received = str(sock.recv(1024), "ascii")
                                received_list.append(received)
                                received_split = received.split(" ")
                                if received_split[0] == "MassReading" and received_split[1] >= data_split[1]:
                                    break


            else:
                sock.send(data)
                #time.sleep(3)
                received = str(sock.recv(1024), "ascii")
                received_list.append(received)





        return(received_list)


def GetMassSpectrum(convertion_coefficient,ip_adress="169.254.198.174"):
    RawInput = SendPacketsToRGA(('Control  "MyProgram" "1.0"','FilamentControl On','AddBarchart Bar1 1 100 PeakCenter 5 0 0 0','scanadd Bar1','ScanStart 1','__wait_for_given_mass__ 100 0','Release'),ip_adress)
    Spectrum = list()  # spectrum is a list of PPM's corresponding to integer molar masses

    for line in RawInput:
        #print(line)
        split_line = line.split()
        if "MassReading" in line:

            MassReadingPosition = split_line.index("MassReading") # in rare cases mass reading os not the zeroth element in list. Finding position of "MassReading" in line is a workaround
            split_eng_notation = (split_line[MassReadingPosition+2]).split("e")  #output is given as engineering notation and need to be interpreted to readable form


            power = 10**(int(split_eng_notation[1]))


            end_result = (float(split_eng_notation[0])*power)*convertion_coefficient  # convertion of engineering notation to readable form. Covertion cooficient is used for unit convertion

            Spectrum.append(end_result)
    return Spectrum



def AppendSpectrumJSON(filename,convertion_coefficient,ip_adress="169.254.198.174"):  # function to get spectrum from spectrometer and append it to given JSON file
    Spectrum = GetMassSpectrum(convertion_coefficient,ip_adress)  # spectrum is obtained by making request to mass spectrometer

    handle = open(filename,"a")

    current_time = int(datetime.datetime.now().timestamp())
    line_to_append = {"class":"spectrum","time":current_time,"array":Spectrum}
    formatted_line = json.dumps(line_to_append)  # current time in computer format and array of PPM's are recorded into JSON formatted line

    handle.write("\n")
    handle.write(formatted_line)
    handle.close()



def GetNonIntegerMassSpectrum(convertion_coefficient,start_mass,amount_of_scans,step,ip_adress="169.254.198.174"):
    packages_list = ['Control  "MyProgram" "1.0"' , 'FilamentControl On']
    for i in range(amount_of_scans):
        packages_list.append(f'AddSinglePeak SinglePeak{i} {start_mass+i*step} 5 0 0 0')
        packages_list.append(f'scanadd SinglePeak{i}')
    packages_list.append('ScanStart 1')
    packages_list.append('__wait_for_given_mass__ 40.95 0')
    packages_list.append( 'Release')


    RawInput = SendPacketsToRGA(packages_list,ip_adress)


    Spectrum = list()  # spectrum is a list of PPM's corresponding to integer molar masses

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

            Spectrum.append(end_result)
    return Spectrum


def AppendNonIntegerSpectrumJSON(filename,convertion_coefficient,start_mass,amount_of_scans,step,ip_adress="169.254.198.174"):  # function to get spectrum from spectrometer and append it to given JSON file
    Spectrum = GetNonIntegerMassSpectrum(convertion_coefficient,start_mass,amount_of_scans,step,ip_adress)  # spectrum is obtained by making request to mass spectrometer

    handle = open(filename,"a")

    current_time = int(datetime.datetime.now().timestamp())
    line_to_append = {"class":"spectrum","time":current_time,"array":Spectrum}
    formatted_line = json.dumps(line_to_append)  # current time in computer format and array of PPM's are recorded into JSON formatted line

    handle.write("\n")
    handle.write(formatted_line)
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



#AppendNonIntegerSpectrumJSON('AnalogSpectrum',1,39,64,0.03125,"169.254.198.174")

#Output = SendPacketsToRGA( ('Control  "MyProgram" "1.0"','FilamentControl On','AddSinglePeak Peak1 37.5 5 0 0 0','scanadd Peak1','ScanStart 1','__listen__ 20 0','Release') )



#Output = SendPacketsToRGA( ('Control  "MyProgram" "1.0"','FilamentControl On','AddBarchart Bar1 1 100 PeakCenter 5 0 0 0','scanadd Bar1','ScanStart 1','__listen__ 100 0','Release') )
#Output = SendPacketsToRGA( ('Control  "MyProgram" "1.0"','FilamentControl On','AddBarchart Bar1 1 100 PeakCenter 5 0 0 0','scanadd Analog1','ScanStart 1','__listen__ 100 0','Release') )

#for element in Output:
 #   print(element)

#TestSpectrum = GetMassSpectrum(1)
#print(TestSpectrum)

