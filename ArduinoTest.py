import time
#import serial
import subprocess
import os
import serial
from JSONoperators import ReadJSONConfig
from JSONoperators import assert_file_exists
import math
import datetime
import json
import datetime
import serial.tools.list_ports

#PORT = '/dev/ttyUSB0'  #"COM7"
#MKS_ADDRESS = "253"


def SendCommand(PORT,command):

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

    print(str(ret).split("!"))

    return ret

if __name__ == "__main__":
    SendCommand("/dev/ttyUSB0","RV!")