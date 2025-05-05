import time
#import serial
import subprocess
import os
import serial

import JSONoperators
from JSONoperators import ReadJSONConfig
from JSONoperators import assert_file_exists
import math
import datetime
import json
import datetime
import serial.tools.list_ports
import Logging

#PORT = '/dev/ttyUSB0'  #"COM7"
#MKS_ADDRESS = "253"


def SendCommand(PORT,command):
    Logging.MakeLogEntry("Communication with arduino board initiated")

    #ports = serial.tools.list_ports.comports()
    #print(ports)

    ser = serial.Serial()
    ser.port = PORT
    ser.baudrate = 9600
    ser.timeout = 10


    ser.open()




    ser.write(command.encode("ascii"))

    time.sleep(0.1)

    ret = ser.read_until(b"!QRT")

    #print(str(ret).split("!"))

    Logging.MakeLogEntry("Communication with arduino board finished")

    return ret


def GetReadingsData():

    PORT = JSONoperators.ReadJSONConfig("arduino","port")
    polynomes = JSONoperators.ReadJSONConfig("arduino","polynomes")

    ret = str(SendCommand(PORT,"RV!"))
    retsplit = ret.split("!")

    print(retsplit)
    raw_voltages =[ retsplit[2],retsplit[4],retsplit[6],retsplit[8],retsplit[10],retsplit[12] ]

    ret_data = []

    for i in range(6):
        ret_data.append( int(raw_voltages[i])*(polynomes[i])[0] + (polynomes[i])[1] )

    return(ret_data)


def LogArduinoData():

    ret_data = GetReadingsData()

    filename = ReadJSONConfig("arduino", "arduino_log_name")
    current_time = int(datetime.datetime.now().timestamp())

    assert_file_exists(filename)

    dictionary_to_append = {}
    dictionary_to_append["time"] = current_time
    dictionary_to_append["pressure"] = [ ret_data[0], ret_data[1]  ]
    dictionary_to_append["temperature"] = [ ret_data[2], ret_data[3], ret_data[4], ret_data[5]   ]

    handle = open(filename, "a")
    handle.write("\n")
    handle.write(json.dumps(dictionary_to_append))
    handle.close()










if __name__ == "__main__":
    LogArduinoData()