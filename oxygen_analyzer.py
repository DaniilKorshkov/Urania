import usb.core
import usb.util
import time
#import serial
import subprocess
import os
import serial
from JSONoperators import ReadJSONConfig
import math
import datetime
import JSONoperators as js

PORT = "/dev/ttyUSB0"

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
        ser.close()  # if connection is already opened, it gets closed
    except:
        pass
    ser.open()   # open connection



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

    return ret

# Message is formatted as following: ST, 1.234  ppm

def GetOxygenData(MainConfig):
    port = js.ReadJSONConfig("ox_an","port",MainConfig)


    while True:  # there is +- 5% chance that output is not formatted properly. If so, the message is discarded
        raw_output = SendCommand(port)
        split_output = raw_output.split(",")
        if split_output[0] == "ST":
            break


    # split_output[0] is ST, split_output[1] is 1.234 ppm

    st_position = split_output.index("ST")


    value = (split_output[st_position+1])
    ret = value.split()[0]  # split_output[1] is splitted into numerical value and PPM(or %)

    if value.split()[1] == "ppm":
        pass
    else:
        ret = ret * 10000  # if value is not in ppm, %'s are converted to ppm
    return ret



