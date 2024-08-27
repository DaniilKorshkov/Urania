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

    return ret



def GetOxygenData(MainConfig):
    port = js.ReadJSONConfig("ox_an","port")

    raw_output = SendCommand(port)

    st_position = raw_output.find("ST,")


    ret = float(  raw_output[ (st_position+4):(st_position+8) ]  )
    
    if "%" in raw_output:
        ret = ret * 10000 # convert % to ppm

    return ret



