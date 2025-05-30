import os

import pyvisa
from pyvisa.constants import StopBits, Parity
import JSONoperators as js
import Logging
import datetime

def switch_valve_position(position, config="MainConfig"):
    Logging.MakeLogEntry("Communication with MIV initiated",log_name="USB_Log")
    motor_address = js.ReadJSONConfig("vicimotor","address")

    timeout_countdown_starter = datetime.datetime.now().timestamp()

    while datetime.datetime.now().timestamp() - timeout_countdown_starter < 20:

        try:
            handle = open(".VICI_USB_LOCK", "r")
            handle.close()
        except:

            handle = open(".VICI_USB_LOCK", 'w')
            handle.close()

            rm = pyvisa.ResourceManager()
            vicivalve = rm.open_resource(motor_address, baud_rate=9600, data_bits=8, parity=Parity.none, stop_bits=StopBits.one,open_timeout=10)

            vicivalve.write("GO"+str(position))

            vicivalve.close()
            os.system("rm .VICI_USB_LOCK")
            Logging.MakeLogEntry("Communication with MIV finished", log_name="USB_Log")

            return None


        Logging.MakeLogEntry("Communication with MIV failed due to timeout",log_name="USB_Log")

