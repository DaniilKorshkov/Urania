import pyvisa
from pyvisa.constants import StopBits, Parity
import JSONoperators as js

def switch_valve_position(position, config="MainConfig"):

    motor_address = js.ReadJSONConfig("vicimotor","address")

    rm = pyvisa.ResourceManager()
    vicivalve = rm.open_resource(motor_address, baud_rate=9600, data_bits=8, parity=Parity.none, stop_bits=StopBits.one,open_timeout=10)

    vicivalve.write("GO"+str(position))

