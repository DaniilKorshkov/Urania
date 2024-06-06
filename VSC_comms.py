import usb.core
import usb.util
import time
#import serial
import subprocess
import os


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









'''def SendCommandToVSC(command):
    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

    ser.isOpen()

    ser.write(command+"\r\n")'''





SendCommandToVSC(f"@005QMD5!Open;FF")
