from TaskManagement import MakeScan, GetTask, GetTaskData
import servo_motor
import time
import RGA_comms
import VSC_comms
import ArduinoComms



def MakeMultiplePurges( purge_cycles_list=[3,4,5] , time_open_list=[25,30,35,40,45] , time_closed_list = [30,35,40,45,50] , pure_line = 14, contaminant_line = 8, calmdown_time = 30, scan_amount = 3 ):
    taskname = GetTask()
    filename,amount_of_scans, valve_position, accuracy, purge_cycles_placeholder = GetTaskData(taskname)

    VSC_comms.ChangeMFCMode("Open")

    for purge_cycles in purge_cycles_list:
        for time_open in time_open_list:
            for time_closed in time_closed_list:




                ArduinoComms.SamplingActOpen()
                servo_motor.switch_valve_position(contaminant_line)
                time.sleep(60)     #introduce contaminant into the line
                ArduinoComms.SamplingActClose()




                servo_motor.switch_valve_position(pure_line)

                for j in range(purge_cycles):
                    ArduinoComms.SamplingActOpen()
                    VSC_comms.LogVSCData()
                    time.sleep(time_open)          
                    ArduinoComms.SamplingActClose()
                    time.sleep(time_closed)

                time.sleep(calmdown_time)

                for i in range(scan_amount):
                    spectrum_to_analyze, intital_mass, step, ErrorMessage = RGA_comms.AppendSpectrumJSON(filename, accuracy=accuracy, custom_line_name = f"PC: {purge_cycles}, TO: {time_open}, TC: {time_closed}")




if __name__ == "__main__":
    MakeMultiplePurges()

