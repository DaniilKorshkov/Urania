import oxygen_analyzer as ox
import VSC_comms as vsc
import subprocess
import JSONoperators as js

def find_ttyUSB_connections():         # function that returns a list of all ttyUSB* elements in /deb
    ttyUSB_list = []
    ret = subprocess.check_output("ls",cwd="/dev",)
    ret = str(ret)
    allUSB_list = ret.split("\\n")

    #print(allUSB_list)

    #print("456")
    for element in allUSB_list:
        print(element)
        if "ttyUSB" in element:
            ttyUSB_list.append(element)


    return ttyUSB_list



def CheckIfVSC(ttyusb_port):
    try:
        address = js.ReadJSONConfig("vsc", "address", "MainConfig")
        vsc_serial_port = ttyusb_port
        pressure_gauge_port = js.ReadJSONConfig("vsc", "pressure_gauge_port", "MainConfig")

        raw_pressure = str(vsc.SendCommand(address, vsc_serial_port, f"PR{pressure_gauge_port}?"))

        ret = vsc.ConvertEngineerNotation(raw_pressure)

        ret = float(ret)

        return True

    except:
        return False



def CheckIfOA(ttyusb_port):
    port = ttyusb_port
    try:

        raw_output = ox.SendCommand(port)
        assert "RA-CAL" in raw_output

        return True

    except:
        return False



def Assign_ttyUSB():
    ttyUSB_list = find_ttyUSB_connections()
    assigned_list = []

    oa_port = None
    vsc_port = None
    miv_port = None



    assert len[ttyUSB_list] == 3

    for element in ttyUSB_list:
        if CheckIfVSC(element):
            ttyUSB_list.remove(element)
            vsc_port = element
            break

    assert len(ttyUSB_list) == 2

    for element in ttyUSB_list:
        if CheckIfOA(element):
            ttyUSB_list.remove(element)
            oa_port = element
            break


    assert len(ttyUSB_list) == 1
    miv_port = ttyUSB_list[0]

    print(f"miv: {miv_port}, vsc: {vsc_port}, oa: {oa_port}")
