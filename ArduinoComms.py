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
import usb

#PORT = '/dev/ttyUSB0'  #"COM7"
#MKS_ADDRESS = "253"


def SendCommand(PORT,command):
    #Logging.MakeLogEntry("Communication with arduino board initiated",log_name="USB_Log")

    #ports = serial.tools.list_ports.comports()
    #print(ports)

    ser = serial.Serial()
    ser.port = PORT
    ser.baudrate = 9600
    ser.timeout = 10

    

    

        

            
    try:
        ser.close()
    except:
        pass
        
    ser.open()




    ser.write(command.encode("ascii"))

    time.sleep(0.1)

    ret = ser.read_until(b"!END")

    ser.close()

    

    #print(str(ret).split("!"))
    ser.close()

    #Logging.MakeLogEntry(f"Communication with arduino board finished with result: {ret}",log_name="USB_Log")
    return ret

    




def GetReadingsData():

    PORT = JSONoperators.ReadJSONConfig("arduino","port")
    polynomes = JSONoperators.ReadJSONConfig("arduino","polynomes")


    ret = str(SendCommand(PORT,"RV"))
    retsplit = ret.split("!")

    print(f"Arduino ret: {ret}")





    raw_voltages =[ retsplit[2],retsplit[4],retsplit[6],retsplit[8],retsplit[10],retsplit[12] ]
    avg_raw_voltages = []

    for element in raw_voltages:
        avg_voltage = float(0)
        array = element.split("+")
        for value in array:
            avg_voltage += float (int(value) / len(array) )
        
        avg_raw_voltages.append(avg_voltage)
        

    ret_data = []

    for i in range(6):
        ret_data.append((avg_raw_voltages[i])*((polynomes[i])[0]) + ((polynomes[i])[1]) )

    for i in range(2):
        ret_data.append( retsplit[14 + 2*i] )

    return ret_data


def LogArduinoData():

    ret_data = GetReadingsData()


    filename = ReadJSONConfig("arduino", "arduino_log_name")
    polynomes = ReadJSONConfig("arduino", "polynomes")
    current_time = int(datetime.datetime.now().timestamp())

    assert_file_exists(filename)

    dictionary_to_append = {}
    dictionary_to_append["time"] = current_time



    dictionary_to_append["PT-01"] = ret_data[0]
    dictionary_to_append["PT-02"] = ret_data[1]
    dictionary_to_append["PT-03"] = ret_data[2]
    dictionary_to_append["PT-04"] = ret_data[3]
    dictionary_to_append["PT-05"] = ret_data[4]
    dictionary_to_append["PT-06"] = ret_data[5]

    if ret_data[6] == 1:
        dictionary_to_append["actuator_one_status"] = "open"
    else:
        dictionary_to_append["actuator_one_status"] = "closed"


    if ret_data[7] == 1:
        dictionary_to_append["actuator_two_status"] = "open"
    else:
        dictionary_to_append["actuator_two_status"] = "closed"


    handle = open(filename, "a")
    handle.write("\n")
    handle.write(json.dumps(dictionary_to_append))
    handle.close()




def TurnActuatorOneOn():

    PORT = JSONoperators.ReadJSONConfig("arduino", "port")
    void = str(SendCommand(PORT, "ACT_ONE_ON"))


def TurnActuatorOneOff():

    PORT = JSONoperators.ReadJSONConfig("arduino", "port")
    void = str(SendCommand(PORT, "ACT_ONE_OFF"))


def TurnActuatorTwoOn():

    PORT = JSONoperators.ReadJSONConfig("arduino", "port")
    void = str(SendCommand(PORT, "ACT_TWO_ON"))


def TurnActuatorTwoOff():

    PORT = JSONoperators.ReadJSONConfig("arduino", "port")
    void = str(SendCommand(PORT, "ACT_TWO_OFF"))



def PingArduino():

    try:
        PORT = JSONoperators.ReadJSONConfig("arduino", "port")
        ret = str(SendCommand(PORT, "PING"))
        retsplit = ret.split("!")
        if retsplit[1] == "THIS_IS_ARDUINO":
            return True
        else:
            return False
    except:
        return False








def NewSendCommand(VID, PID, command):




    dev = usb.core.find(idVendor = int(VID, base=16), idProduct = int(PID, base=16))

    reattach = False
    if dev.is_kernel_driver_active(0):
        reattach = True
        dev.detach_kernel_driver(0)


    dev.set_configuration()


    cfg = dev.get_active_configuration()
    intf = cfg[0,0]
    ser = intf[1]
    print(ser)




    assert ser is not None

    Logging.MakeLogEntry("Communication with arduino board initiated", log_name="USB_Log")

    # ports = serial.tools.list_ports.comports()
    # print(ports)



    timeout_countdown_starter = datetime.datetime.now().timestamp()

    while datetime.datetime.now().timestamp() - timeout_countdown_starter < 20:

        try:
            handle = open(".ARD_USB_LOCK", "r")
            handle.close()
        except:

            handle = open(".ARD_USB_LOCK", 'w')
            handle.close()



            ser.write(command.encode("ascii"))

            time.sleep(0.1)

            ret = ser.read_until(b"!END")

            ser.close()

            os.system("rm .ARD_USB_LOCK")

            # print(str(ret).split("!"))
            ser.close()

            Logging.MakeLogEntry(f"Communication with arduino board finished with result: {ret}", log_name="USB_Log")
            usb.util.dispose_resources(dev)
            if reattach:
                dev.attach_kernel_driver(0)
            return ret

        Logging.MakeLogEntry(f"Communication with arduino board failed due to timeout", log_name="USB_Log")
        return None



def NewPingArduino():


        VID = JSONoperators.ReadJSONConfig("arduino", "VID")
        PID = JSONoperators.ReadJSONConfig("arduino", "PID")
        ret = str(NewSendCommand(VID,PID, "PING"))
        retsplit = ret.split("!")
        if retsplit[1] == "THIS_IS_ARDUINO":
            return True
        else:
            return False



if __name__ == "__main__":
    print(GetReadingsData())