from TaskManagement import MakeScan, GetTask, GetTaskData
import servo_motor



def MakeMultiplePurges():
    taskname = GetTask()
    spectrum_filename,amount_of_scans, valve_position, accuracy, purge_cycles = GetTaskData(taskname)

    for i in range(9):

        VSC_comms.ChangeMFCMode("Open")
        servo_motor.switch_valve_position(8)
        time.sleep(60)     #introduce contaminant into the line
        VSC_comms.ChangeMFCMode("Close")



        for j in range(purge_cycles):
            VSC_comms.ChangeMFCMode("Open")
            ArduinoComms.TurnActuatorOneOn()
            VSC_comms.LogVSCData()
            time.sleep(35)
            VSC_comms.ChangeMFCMode("Close")
            ArduinoComms.TurnActuatorOneOff()
            time.sleep(30)
        time.sleep(30)


