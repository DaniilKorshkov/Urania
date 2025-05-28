import random

import usb.core
import usb.util
import time
#import serial
import subprocess
import os
import serial

import Logging
from JSONoperators import ReadJSONConfig
from JSONoperators import assert_file_exists
import math
import datetime
import json
import datetime
import ArduinoComms
import random

#PORT = '/dev/ttyUSB0'  #"COM7"
#MKS_ADDRESS = "253"


def SendCommand(MKS_ADDRESS,PORT,command):  #function to send command to VSC via Serial port

    Logging.MakeLogEntry("Communication with VSC initiated",log_name="USB_Log")

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
    except:
        pass
    ser.open()



    ser.write(bytes(f"@{MKS_ADDRESS}{command};FF", "ascii"))

    #print("data sent !!!")

    time.sleep(0.1)

    result = ser.read_until(b"FF")

    ser.close()
    Logging.MakeLogEntry(f"Communication with VSC finished with reading {result}",log_name="USB_Log")

    return result


def ReadMFMFlowRate(MainConfig="MainConfig"):  # Function to read flow rate (ml/min) from Mass Flow Meter


    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfm_port = ReadJSONConfig("vsc","mfm_port",MainConfig)

    raw_flowrate = str(SendCommand(address,vsc_serial_port,f"FR{mfm_port}?"))
    #print(raw_flowrate)

    ret = ConvertEngineerNotation(raw_flowrate)


    return ret



def ReadFillingMFMFlowRate(MainConfig="MainConfig"):  # Function to read flow rate (ml/min) from Mass Flow Meter


    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfm_port = ReadJSONConfig("vsc","filling_mfm_port",MainConfig)

    raw_flowrate = str(SendCommand(address,vsc_serial_port,f"FR{mfm_port}?"))
    #print(raw_flowrate)

    ret = ConvertEngineerNotation(raw_flowrate)



    return ret




def ReadPressureGauge(MainConfig="MainConfig"): # Function to read pressure (torr or pascal???) from pressure gauge


    address = ReadJSONConfig("vsc", "address", MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc", "vsc_serial_port")
    pressure_gauge_port = ReadJSONConfig("vsc", "pressure_gauge_port", MainConfig)

    raw_pressure = str(SendCommand(address, vsc_serial_port, f"PR{pressure_gauge_port}?"))


    ret = ConvertEngineerNotation(raw_pressure)



    return ret



def ReadMFCFlowRate(MainConfig="MainConfig"):  # Function to read flow rate (ml/min) from Mass Flow Controller


    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfc_port = ReadJSONConfig("vsc","mfc_port",MainConfig)

    raw_flowrate = str(SendCommand(address,vsc_serial_port,f"FR{mfc_port}?"))
    #print(raw_flowrate)

    ret = ConvertEngineerNotation(raw_flowrate)

    return ret


def ReadMFCSetpoint(MainConfig="MainConfig"):  # Function to read flow rate (ml/min) from Mass Flow Controller
    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfc_port = ReadJSONConfig("vsc","mfc_port",MainConfig)

    raw_flowrate = str(SendCommand(address,vsc_serial_port,f"QSP{mfc_port}?"))
    #print(raw_flowrate)

    ret = ConvertEngineerNotation(raw_flowrate)

    return ret




def ChangeMFCMode(mode,MainConfig="MainConfig"):  # Function to change mode of Mass Flow Controller (open/close/setpoint)
    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfc_port = ReadJSONConfig("vsc","mfc_port",MainConfig)

    assert mode == "Open" or mode == "Close" or mode == "Setpoint"

    void = SendCommand(address,vsc_serial_port,f"QMD{mfc_port}!{mode}")
    print(f"QMD{mfc_port}!{mode}")
    print(void)


def ReadMFCMode(MainConfig="MainConfig"):  # Function to read flow rate (ml/min) from Mass Flow Controller
    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfc_port = ReadJSONConfig("vsc","mfc_port",MainConfig)

    mode = str(SendCommand(address,vsc_serial_port,f"QMD{mfc_port}?"))

    if "OPEN" in str(mode):
        ret = "Open"
    if "CLOSE" in str(mode):
        ret = "Closed"
    if "SETPOINT" in str(mode):
        ret = "Setpoint"

    return ret


def ChangeMFCFlowRate(newflowrate,MainConfig="MainConfig"):   # Change flow rate of Mass Flow Controller
    address = ReadJSONConfig("vsc", "address", MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc", "vsc_serial_port")
    mfc_port = ReadJSONConfig("vsc", "mfc_port", MainConfig)

    assert newflowrate >= 0

    if newflowrate == 0:
        ChangeMFCMode("Close",MainConfig)
    else:
        converted_flowrate =ConvertToEngNotation(newflowrate)

        void = SendCommand(address, vsc_serial_port, f"QSP{mfc_port}!{converted_flowrate}")
        print(f"QSP{mfc_port}!{converted_flowrate}")
        print(void)


def ChangePCMode(mode,MainConfig="MainConfig"):   # Change mode of pressure controller (open/close/setpoint)
    address = ReadJSONConfig("vsc", "address", MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc", "vsc_serial_port")
    pc_port = ReadJSONConfig("vsc", "pressure_controller_port", MainConfig)

    assert mode == "Open" or mode == "Close" or mode == "Setpoint"

    void = SendCommand(address, vsc_serial_port, f"QMD{pc_port}!{mode}")
    print(void)




def ChangePCPressure(newpressure,MainConfig="MainConfig"):  # Change pressure of pressure controller
    address = ReadJSONConfig("vsc", "address", MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc", "vsc_serial_port")
    pc_port = ReadJSONConfig("vsc", "pressure_controller_port", MainConfig)

    assert newpressure >= 0

    if newpressure == 0:
        ChangePCMode("Close", MainConfig)
    else:
        converted_pressure = ConvertToEngNotation(newpressure)

        void = SendCommand(address, vsc_serial_port, f"QSP{pc_port}!{converted_pressure}")
        print(void)



def ReadPCPressure(MainConfig="MainConfig"):  # Read pressure from pressure controller
    address = ReadJSONConfig("vsc", "address", MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc", "vsc_serial_port")
    pressure_controller_port = ReadJSONConfig("vsc", "pressure_controller_port", MainConfig)

    raw_pressure = str(SendCommand(address, vsc_serial_port, f"PR{pressure_controller_port}?"))


    ret = ConvertEngineerNotation(raw_pressure)

    return ret


def ReadPCSetpoint(MainConfig="MainConfig"):  # Function to read flow rate (ml/min) from Mass Flow Controller
    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    pc_port = ReadJSONConfig("vsc","pressure_controller_port",MainConfig)

    raw_flowrate = str(SendCommand(address,vsc_serial_port,f"QSP{pc_port}?"))
    #print(raw_flowrate)

    ret = ConvertEngineerNotation(raw_flowrate)

    return ret


def ReadPCMode(MainConfig="MainConfig"):   # Change mode of pressure controller (open/close/setpoint)
    address = ReadJSONConfig("vsc", "address", MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc", "vsc_serial_port")
    pc_port = ReadJSONConfig("vsc", "pressure_controller_port", MainConfig)



    mode = SendCommand(address, vsc_serial_port, f"QMD{pc_port}?")
    if "OPEN" in str(mode):
        ret = "Open"
    if "CLOSE" in str(mode):
        ret = "Closed"
    if "SETPOINT" in str(mode):
        ret = "Setpoint"

    return ret





def ConvertEngineerNotation(raw_message):  # Function to exctract number from message and convert it from eng notation (d.ddE+pp) to normal number
    if "ACK" in raw_message:
        k_position = raw_message.find("K")
        e_position = raw_message.find("E")
        semicolomn_position = raw_message.find(";")

        real_part = raw_message[(k_position+1):(e_position)]
        real_part = real_part.strip(">")
        real_part = real_part.strip("<")

        #print(real_part)
        power = raw_message[(e_position+1):(semicolomn_position)]
        #print(power)
        rdy_number = float(real_part)*(10**int(power))

        return rdy_number



def ConvertToEngNotation(number):  # function to convert normal number to engineer notation
    log = math.log10(number)
    print(log)
    if log >= 0:
        final_log = int(log)
        print(final_log)
        unrounded_number = float(number/(10**final_log))
        print(unrounded_number)
        final_number = round(unrounded_number, 3)
        return(f"{final_number}E+{final_log}")
    else:
        if log%1 == 0:
            final_log = int(log)
        else:
            final_log = int(log) - 1
        unrounded_number = number / (10 ** final_log)
        final_number = round(unrounded_number, 2)
        return (f"{final_number}E{final_log}")



def StabilizePressure(MainConfig="MainConfig"):
    ChangeMFCMode("Setpoint")
    current_pressure = ReadPCPressure(MainConfig)
    current_flow = ReadMFCFlowRate(MainConfig)

    while current_pressure < 750:
        if current_pressure > 500:

            if current_flow*0.9 > 20:
                ChangeMFCFlowRate(current_flow*0.9)
            time.sleep(5)
            current_pressure = ReadPCPressure(MainConfig)
            current_flow = ReadMFCFlowRate(MainConfig)

            if current_flow < 25:
                ChangeMFCMode("Close")
                break

        else:

            if current_flow*0.8>20:
                ChangeMFCFlowRate(current_flow * 0.8)
            time.sleep(2.5)
            current_pressure = ReadPCPressure(MainConfig)
            current_flow = ReadMFCFlowRate(MainConfig)
            if current_flow < 25:
                ChangeMFCMode("Close")
                break



def IncreaseFlowRate(MainConfig="MainConfig"):
    ChangeMFCMode("Setpoint")
    theoretical_flow = ReadMFCFlowRate(MainConfig)

    while True:
        current_flow = ReadMFCFlowRate(MainConfig)
        theoretical_flow = theoretical_flow*1.05
        if theoretical_flow < 20:
            theoretical_flow = 20
        ChangeMFCFlowRate(theoretical_flow)
        time.sleep(7.5)
        current_pressure = ReadPCPressure(MainConfig)
        if current_pressure < 755:
            if current_flow > 20:
                ChangeMFCFlowRate(theoretical_flow*0.952)
            else:
                ChangeMFCMode("Close")
            break


def StabilityWatcher():
    last_stabilize = datetime.datetime.now().timestamp()
    last_increase = datetime.datetime.now().timestamp()

    while True:

        try:

            if datetime.datetime.now().timestamp() - last_stabilize > 1:
                current_pressure = ReadPCPressure()
                if current_pressure < 750:

                    StabilizePressure()
                    print("Stabilized!!!")
                    time.sleep(10)
                    IncreaseFlowRate()

            if datetime.datetime.now().timestamp() - last_increase > 60:

                IncreaseFlowRate()

        except:
            pass



def SmartCloseMFC(MainConfig="MainConfig"):
    CurrentFlow = ReadMFCFlowRate(MainConfig)
    FlowToSet = 2.341*CurrentFlow - 1241
    if FlowToSet < 20:
        ChangeMFCMode("Close")
    else:
        ChangeMFCMode("Setpoint")
        ChangeMFCFlowRate(FlowToSet)




def FullQuery(MainConfig="MainConfig"):
    pg_port = ReadJSONConfig("vsc", "pressure_gauge_port")
    pc_port = ReadJSONConfig("vsc", "pressure_controller_port")
    mfc_port = ReadJSONConfig("vsc", "mfc_port")
    mfm_port = ReadJSONConfig("vsc", "mfm_port")

    print(f"\n")
    print(f"Make sure that pressure meter is connected to port {pg_port}, pressure controller to {pc_port}, mfc to {mfc_port}, mfm to {mfm_port}")
    print(f"\n")


    print(f"Pressure Meter Data: ")
    pressure = ReadPressureGauge(MainConfig)
    print(f"Current pressure at common line: {pressure}")

    print(f"\n")

    print(f"Mass Flow Controller Data: ")
    mass_flow = ReadMFCFlowRate(MainConfig)
    mode = ReadMFCMode(MainConfig)
    setpoint = ReadMFCSetpoint(MainConfig)
    print(f"Current mode: {mode}")
    print(f"Current mass flow: {mass_flow}")
    print(f"Current setpoint: {setpoint}")

    print(f"\n")

    print(f"Pressure Controller Data: ")
    pressure = ReadPCPressure(MainConfig)
    mode = ReadPCMode(MainConfig)
    setpoint = ReadPCSetpoint()
    print(f"Current mode: {mode}")
    print(f"Current pressure: {pressure}")
    print(f"Current setpoint: {setpoint}")

    print(f"\n")

    print(f"Mass Flow Meter Data: ")
    mass_flow = ReadMFMFlowRate(MainConfig)
    print(f"Current mass flow: {mass_flow}")

    print(f"\n")

    try:
        filling_mfm_flow = ReadFillingMFMFlowRate(MainConfig)
    except:
        filling_mfm_flow = 0

    print(f"Current mass flow for filling station: {filling_mfm_flow}")
    print(f"\n")

def LogVSCData(MainConfig="MainConfig"):
    #pg_port = ReadJSONConfig("vsc", "pressure_gauge_port")
    #pc_port = ReadJSONConfig("vsc", "pressure_controller_port")
    #mfc_port = ReadJSONConfig("vsc", "mfc_port")
    #mfm_port = ReadJSONConfig("vsc", "mfm_port")
    filename = ReadJSONConfig("vsc","vsc_log_name")

    assert_file_exists(filename)

    pg_pressure = ReadPressureGauge(MainConfig)
    
    mfc_flow = ReadMFCFlowRate(MainConfig)
    mfc_mode = ReadMFCMode(MainConfig)
    mfc_setpoint = ReadMFCSetpoint(MainConfig)
    
    pc_pressure = ReadPCPressure(MainConfig)
    pc_mode = ReadPCMode(MainConfig)
    pc_setpoint = ReadPCSetpoint(MainConfig)
    
    mfm_flow = ReadMFMFlowRate(MainConfig)

    try:
        filling_mfm_flow = ReadFillingMFMFlowRate(MainConfig)
    except:
        filling_mfm_flow = 0
    
    
    current_time = int(datetime.datetime.now().timestamp())
    dictionary_to_append = {}
    dictionary_to_append["time"] = current_time
    
    dictionary_to_append["pg_pressure"] = pg_pressure
    
    dictionary_to_append["mfc_flow"] = mfc_flow
    dictionary_to_append["mfc_mode"] = mfc_mode
    dictionary_to_append["mfc_setpoint"] = mfc_setpoint
    
    dictionary_to_append["pc_pressure"] = pc_pressure
    dictionary_to_append["pc_mode"] = pc_mode
    dictionary_to_append["pc_setpoint"] = pc_setpoint
    
    dictionary_to_append["mfm_flow"] = mfm_flow

    dictionary_to_append["filling_mfm_flow"] = filling_mfm_flow
    
    
    
    handle = open(filename, "a")
    handle.write("\n")
    handle.write(json.dumps(dictionary_to_append))
    handle.close()


    
    
    
    
    
if __name__ == "__main__":
    filename = ReadJSONConfig("vsc", "vsc_log_name")

    assert_file_exists(filename)


    filling_mfm_flow = random.randint(10,20)

    current_time = int(datetime.datetime.now().timestamp())
    dictionary_to_append = {}
    dictionary_to_append["time"] = current_time

    dictionary_to_append["filling_mfm_flow"] = filling_mfm_flow

    handle = open(filename, "a")
    handle.write("\n")
    handle.write(json.dumps(dictionary_to_append))
    handle.close()


#StabilityWatcher()

