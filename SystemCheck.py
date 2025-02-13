import RGA_comms
import JSONoperators
import VSC_comms
import oxygen_analyzer
import Logging as lg

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
                lg.MakeLogEntry(f"RGA heater status is {heatstat}. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"RGA heater status is {heatstat}. Sampling is cancelled\n")


    if capheatstat != "On":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass cap heater")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Capillary heater status: {capheatstat}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"RGA capillary heater status is {capheatstat}. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"RGA capillary heater status is {capheatstat}. Sampling is cancelled\n")


    if pumpstat != "On":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass pump")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Pump status: {pumpstat}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"RGA pump status is {pumpstat}. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"RGA pump status is {pumpstat}. Sampling is cancelled\n")



    if filament_status[0] != "ON":
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass filament")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Filament status: {filament_status}. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"RGA filament status is {filament_status}. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"RGA filament status is {filament_status}. Sampling is cancelled\n")



    try:
        void = VSC_comms.ReadMFCFlowRate()
    except:
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass MFC")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Cannot reach MFC. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"Cannot reach MFC. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"Cannot reach MFC. Sampling is cancelled\n")


    try:
        void = VSC_comms.ReadMFMFlowRate()
    except:
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass MFM")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Cannot reach MFM. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"Cannot reach MFM. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"Cannot reach MFM. Sampling is cancelled\n")


    try:
        void = VSC_comms.ReadPCPressure()
    except:
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass PC")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Cannot reach pressure controller. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"Cannot reach pressure controller. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"Cannot reach pressure controller. Sampling is cancelled\n")


    try:
        void = VSC_comms.ReadPressureGauge()
    except:
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass PG")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Cannot reach pressure gauge. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"Cannot reach pressure gauge. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"Cannot reach pressure gauge. Sampling is cancelled\n")



    try:
        void = oxygen_analyzer.GetOxygenData()
    except:
        try:
            bypass = JSONoperators.ReadJSONConfig("system_check","bypass OA")
        except:
            bypass = False
        if not bypass:
            manual_bypass = str(input(f"Cannot reach oxygen analyzer. Press 'y' to continue "))
            if manual_bypass.lower()[0] == "y":
                bypass = True
                lg.MakeLogEntry(f"Cannot reach oxygen analyzer. Sampling initiated by user despite this fact")
        if not bypass:
            faliures_found = True
            lg.MakeLogEntry(f"Cannot reach oxygen analyzer. Sampling is cancelled\n")


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