import usb.core
import usb.util
import time
#import serial
import subprocess
import os
import serial
from JSONoperators import ReadJSONConfig


def SendCommandToVSC(command):
    #import usb.core
    #import usb.util
    #os.system("echo '0x0403-0x6001' |sudo tee /sys/bus/usb/drivers/usb/unbind")

    # find our device
    dev = usb.core.find(idVendor=0x0403, idProduct=0x6001)

    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    endpoint = dev[0].interfaces()[0].endpoints()[0]
    i = dev[0].interfaces()[0].bInterfaceNumber

    if dev.is_kernel_driver_active(i):
        try:
            dev.detach_kernel_driver(i)
        except:
            raise ValueError('Cannot reattach driver')

    dev.set_configuration()
    endadress = endpoint.bEndpointAddress





    endpoint.write(bytes(command,"ascii"))
    while True:
        try:
            ret = dev.read(endadress,16)
            print(ret)
        except:
            pass



    #while True:
        #print(dev.read)

def SendCommandThroughSerial():

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

    ser.isOpen()


    #ser.write(bytes(f'@001QMD1Open?;FF','ascii'))

    #ser.close()

    while True:

        bytesline = ser.readline(1)
        print(bytesline)

    '''buffer = bytes()  # .read() returns bytes right?
    while True:

        #if ser.in_waiting:
            buffer += ser.read(1)
            print(buffer)
            try:
                complete = buffer[:buffer.index(b'}') + 1]  # get up to '}'
                buffer = buffer[buffer.index(b'}') + 1:]  # leave the rest in buffer
            except ValueError:
                continue  # Go back and keep reading
                print('error')
            print('buffer=', complete)
            ascii = buffer.decode('ascii')
            print('ascii=', ascii)'''




#SendCommandThroughSerial()

PORT = '/dev/ttyUSB0'  #"COM7"
MKS_ADDRESS = "253"


def SendCommand(MKS_ADDRESS,PORT,command):
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



    ser.write(bytes(f"@{MKS_ADDRESS}{command}?;FF", "ascii"))

    #print("data sent !!!")

    time.sleep(1)

    result = ser.read_until(b"FF")

    return result


def ReadMFMFlowRate(MainConfig="MainConfig"):
    address = ReadJSONConfig("vcs","address",MainConfig)
    vcs_serial_port = ReadJSONConfig("vcs","vcs_serial_port")
    mfm_port = ReadJSONConfig("vcs","mfm_port",MainConfig)
    raw_flowrate = str(SendCommand(address,vcs_serial_port,f"FR{mfm_port}"))
    #print(raw_flowrate)
    if "ACK" in raw_flowrate:
        k_position = raw_flowrate.find("K")
        e_position = raw_flowrate.find("E")
        semicolomn_position = raw_flowrate.find(";")

        real_part = raw_flowrate[(k_position+1):(e_position)]
        #print(real_part)
        power = raw_flowrate[(e_position+1):(semicolomn_position)]
        #print(power)
        rdy_number = float(real_part)*(10**int(power))

        return rdy_number










print(ReadMFMFlowRate())