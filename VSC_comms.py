import usb.core
import usb.util
import time
#import serial
import subprocess
import os
import serial
from JSONoperators import ReadJSONConfig
import math

#PORT = '/dev/ttyUSB0'  #"COM7"
#MKS_ADDRESS = "253"


def SendCommand(MKS_ADDRESS,PORT,command):  #function to send command to VSC via Serial port
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

    time.sleep(1)

    result = ser.read_until(b"FF")

    return result


def ReadMFMFlowRate(MainConfig="MainConfig"):  # Function to read flow rate (ml/min) from Mass Flow Meter
    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfm_port = ReadJSONConfig("vsc","mfm_port",MainConfig)

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




def ChangeMFCMode(mode,MainConfig="MainConfig"):  # Function to change mode of Mass Flow Controller (open/close/setpoint)
    address = ReadJSONConfig("vsc","address",MainConfig)
    vsc_serial_port = ReadJSONConfig("vsc","vsc_serial_port")
    mfc_port = ReadJSONConfig("vsc","mfc_port",MainConfig)

    assert mode == "Open" or mode == "Close" or mode == "Setpoint"

    void = SendCommand(address,vsc_serial_port,f"QMD{mfc_port}!{mode}")
    print(f"QMD{mfc_port}!{mode}")
    print(void)


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
    pressure_gauge_port = ReadJSONConfig("vsc", "pressure_controller_port", MainConfig)

    raw_pressure = str(SendCommand(address, vsc_serial_port, f"PR{pressure_gauge_port}?"))


    ret = ConvertEngineerNotation(raw_pressure)

    return ret





def ConvertEngineerNotation(raw_message):  # Function to exctract number from message and convert it from eng notation (d.ddE+pp) to normal number
    if "ACK" in raw_message:
        k_position = raw_message.find("K")
        e_position = raw_message.find("E")
        semicolomn_position = raw_message.find(";")

        real_part = raw_message[(k_position+1):(e_position)]
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


print(ReadPCPressure())
