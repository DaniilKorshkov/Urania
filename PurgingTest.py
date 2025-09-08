from TaskManagement import MakeScan, GetTask, GetTaskData
import servo_motor



def MakeMultiplePurges():
    taskname = GetTask()
    spectrum_filename,amount_of_scans, valve_position, accuracy, purge_cycles_placeholder = GetTaskData(taskname)

    VSC_comms.ChangeMFCMode("Open")

    for purge_cycles in [3,4,5,6,7]:
        for time_open in [25,30,35,40,45]:
            for time_closed in [30,35,40,45,50]:




                ArduinoComms.SamplingActOpen()
                servo_motor.switch_valve_position(8)
                time.sleep(60)     #introduce contaminant into the line
                ArduinoComms.SamplingActClose()




                servo_motor.switch_valve_position(16)

                for j in range(purge_cycles):
                    ArduinoComms.SamplingActOpen()
                    VSC_comms.LogVSCData()
                    time.sleep(time_open)          
                    ArduinoComms.SamplingActClose()
                    time.sleep(time_closed)
                    
                time.sleep(30)


                spectrum_to_analyze, intital_mass, step, ErrorMessage = RGA_comms.AppendSpectrumJSON(filename, accuracy=accuracy, custom_line_name = f"PC: {purge_cycles}, TO: {time_open}, TC: {time_closed}")




if __name__ == "__main__":
    MakeMultiplePurges()

