import InputValidationLoop as ivl
import Initiation as ini
import pyvisa
from pyvisa.constants import StopBits, Parity
def main():
    keep_running = True
    valves_list, current_valve = ini.initiation()
    current_valve_number = 0

    rm = pyvisa.ResourceManager()
    vicivalve = rm.open_resource('ASRL3::INSTR', baud_rate=9600, data_bits=8, parity=Parity.none, stop_bits=StopBits.one)

    while keep_running:

        print(f"Current valve is: {current_valve}")
        user_command = ivl.get_user_command()
        if user_command == "n":
            current_valve_number = (current_valve_number + 1)%len(valves_list)
            current_valve = valves_list[current_valve_number]
            vicivalve.write("GO"+str(current_valve))
        if user_command == "p":
            current_valve_number = (current_valve_number - 1)%len(valves_list)
            current_valve = valves_list[current_valve_number]
            vicivalve.write("GO" + str(current_valve))
        if user_command == "e":
            print("Goodbye")
            keep_running = False


main()