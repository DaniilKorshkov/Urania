import usb.core
import usb.util
import time
#import serial
import subprocess
import os
import serial

import Logging
from JSONoperators import ReadJSONConfig
import math
import datetime
import JSONoperators as js
import logging



def SendCommand(PORT):  #function to send command to oxygen analyser via Serial port
    ser = serial.Serial(
        port=PORT,
        timeout=10.0,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
    )

    

        

    try:
        ser.close()
        ser.open()
    except:
        ser.open()



    ser.write(bytes(f"st","ascii"))

    ret = ""  # ret is a string, which gets updated and printed every time data received

    for i in range(83):
            result = ser.read()  # data is received from oxygen analyzer
            try:
                result = result.decode("ascii")
                ret=ret+str(result)  # ret appended
            except:
                pass
    #print(ret)   # ret printed
    #splitret = ret.split()
    #for element in splitret:
        #print(element)

    ser.close()

    

    return ret





def GetOxygenData(MainConfig="MainConfig"):
    #Logging.MakeLogEntry("Communication with oxygen analyzer initiated",log_name="USB_Log")
    port = js.ReadJSONConfig("ox_an","port",MainConfig)


    while True:
        raw_output = SendCommand(port)
        split_output = raw_output.split(",")
        if split_output[0] == "ST":
            break





    st_position = split_output.index("ST")




    value = (split_output[st_position+1])
    ret = value.split()[0]
    ret = float(ret)

    if value.split()[1] == "ppm":
        pass
    else:
        ret = ret * 10000

    #Logging.MakeLogEntry(f"Communication with oxygen analyzer finished with result {ret}",log_name="USB_Log")
    return ret




