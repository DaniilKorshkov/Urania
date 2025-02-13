import RGA_comms
import JSONoperators

def SystemCheck(MainConfig="MainConfig"):
    heatstat, capheatstat, pumpstat = RGA_comms.heating_info()
    filament_status = RGA_comms.rga_filament_info()
    #multiplier_status = RGA_comms.rga_multiplier_info()

    faliures_found = False

    if heatstat != "Warm":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass heater")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Heater status: {heatstat}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
        if not bypass:
            faliures_found = True


    if capheatstat != "On":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass cap heater")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Capillary heater status: {capheatstat}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
        if not bypass:
            faliures_found = True


    if pumpstat != "On":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass pump")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Pump status: {pumpstat}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
        if not bypass:
            faliures_found = True



    if filament_status[0] != "ON":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass filament")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Filament status: {filament_status}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
        if not bypass:
            faliures_found = True


    '''if multiplier_status != "Yes":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass multiplier")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Multiplier status: {multiplier_status}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
        if not bypass:
            faliures_found = True'''















    return faliures_found