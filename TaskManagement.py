import json
import datetime

import Logging
import Logging as lg
import JSONoperators as js
import VSC_comms
import servo_motor
import RGA_comms
import VSC_comms as vsc
import time
import os
import AbnormalityReaction as ar
import subprocess
from EmailNotificationSystem import NotifyUser
import ArduinoComms
import signal


"""def TimeoutHandler():
    Logging.MakeLogEntry("Timeout in TaskManagement")
    raise Exception("Timeout")"""

def GetTasklistName(config="MainConfig"):  #function to get name of task list from main config
    tasklist_name = None
    handle = open(config, "r")
    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == "tasks":
            tasklist_name = dict_line["TaskList"]
            default_tasklist_name = dict_line["DefaultTaskList"]
            break
    handle.close()
    return tasklist_name, default_tasklist_name

def UpdateTaskList(tasklist_name,text_to_append):

        handle = open(tasklist_name,"w")
        i = 1
        for line in text_to_append:
            handle.write(line)
            if i < len(text_to_append):
                handle.write("\n")
            i += 1

        handle.close()

def CheckForEmergencyTasks(config="MainConfig"):  #function that reads task list for emergency tasks. Returns True,task_name or False,None
    tasklist_name = js.ReadJSONConfig("tasks","TaskList")

    if tasklist_name == None:
        raise NameError("Task List is not specified in Main Config")

    text_copy = []
    if_task_found = False
    task_to_execute = None

    handle = open(tasklist_name, "r")
    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":   #skip empty lines
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == "task" and dict_line["type"] == "emergency" and not if_task_found:

            try:   # evaluation of executiuon times.
                match dict_line["how_much_executions"]:
                    case "inf":  #infinite executions case
                        text_copy.append(line.strip("\n"))
                        if_task_found = True
                        task_to_execute = dict_line["name"]
                    case 0:  #if 0 execution time left, task is no longer appended to txt file and is deleted
                        pass
                    case _:  # else, howmuchexecutions is decremented by 1
                        howmuchexecutions = int(dict_line["how_much_executions"])-1
                        dict_line["how_much_executions"] = howmuchexecutions
                        text_copy.append(json.dumps(dict_line))
                        if_task_found = True
                        task_to_execute = dict_line["name"]
            except:  #if dict_line["how_much_executions"] not found, it is considered to be 1
                pass
        else:
            text_copy.append(line.strip("\n"))
    handle.close()

    if if_task_found:  # TaskList updated
        UpdateTaskList(tasklist_name,text_copy)

    return if_task_found,task_to_execute

def CheckForScheduledTasks(config="MainConfig"): #function that reads task list for scheduled tasks. Returns True,task_name or False,None

    tasklist_name = js.ReadJSONConfig("tasks", "TaskList")

    if tasklist_name == None:
        raise NameError("Task List is not specified in Main Config")

    current_time = int(datetime.datetime.now().timestamp())
    task_to_execute = None
    if_scheduled_tasks = False

    text_copy = []

    handle = open(tasklist_name,"r")
    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == "task" and dict_line["type"] == "scheduled" and (not if_scheduled_tasks):
            if int(dict_line["last_execution"])+int(dict_line["freq"]) < current_time:
                task_to_execute = dict_line["name"]
                dict_line["last_execution"] = int(datetime.datetime.now().timestamp()) # if scheduled task is found, execution time is updated
                if_scheduled_tasks = True


        text_copy.append(json.dumps(dict_line))

    handle.close()

    if if_scheduled_tasks:  # TaskList updated
        UpdateTaskList(tasklist_name, text_copy)

    return if_scheduled_tasks,task_to_execute


def GetAmountOfRegularTasks(config="MainConfig"):  # function to get amount of regular tasks

    tasklist_name = js.ReadJSONConfig("tasks","TaskList")
    if tasklist_name == None:
        raise NameError("Task List is not specified in Main Config")

    handle = open(tasklist_name)
    regular_tasks_count = 0

    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == "task":
            if dict_line["type"] == "regular":
                regular_tasks_count += 1

    handle.close()
    return regular_tasks_count


def GetRegularTask(config="MainConfig"):  #function to get regular task name

    text_copy = []

    tasklist_name = js.ReadJSONConfig("tasks", "TaskList")
    if tasklist_name == None:
        raise NameError("Task List is not specified in Main Config")
    task_amount = GetAmountOfRegularTasks(config)
    handle = open(tasklist_name,'r')
    for line in handle:
        if line == "" or line == "\n" or line[0] == "#":
            continue
        dict_line = json.loads(line)
        if dict_line["class"] == "regular_log":
            current_task_number = (dict_line["last_executed"] + 1) % task_amount  #number of previously executed task updated
            dict_line["last_executed"] = current_task_number
            text_copy.append(json.dumps(dict_line))
        else:
            text_copy.append(line.strip("\n"))

    handle.close()

    i=0

    handle = open(tasklist_name,'r')
    for line in handle:

        if line == "" or line == "\n" or line[0] == "#":
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == "task":
            if dict_line["type"] == "regular":
                if i == current_task_number:
                    task_to_execute = dict_line["name"]
                i += 1
    handle.close()

    UpdateTaskList(tasklist_name, text_copy)

    return task_to_execute



def GetTask(config="MainConfig"):  # function that checks for emergency tasks; for scheduled tasks, for regular tasks and returns name of required task

    tasklist_name = js.ReadJSONConfig("tasks","TaskList")
    default_tasklist_name = js.ReadJSONConfig("tasks","DefaultTaskList")
    js.assert_file_exists(tasklist_name, default_tasklist_name)

    ifemergencytasks, taskname = CheckForEmergencyTasks(config)
    if not ifemergencytasks:
        ifscheduledtasks, taskname = CheckForScheduledTasks(config)
        if not ifscheduledtasks:
            taskname = GetRegularTask(config)



    return taskname

def GetTaskData(taskname, config="MainConfig"):

    tasklist_name = js.ReadJSONConfig("tasks", "TaskList")
    default_tasklist_name = js.ReadJSONConfig("tasks", "DefaultTaskList")
    js.assert_file_exists(tasklist_name, default_tasklist_name)

    handle = open(tasklist_name)
    for line in handle:
    	
        if line == "" or line == "\n" or line[0] == "#":
            continue
    	
        dict_line = json.loads(line)
        try:
            if dict_line["name"] == taskname:
                spectrum_filename = dict_line["filename"]
                amount_of_scans = dict_line["scans"]
                valve_position = dict_line["valve_position"]


                purging_time = dict_line["purging_time"]
                calmdown_time = dict_line["calmdown_time"]
                purging_mfc = dict_line["purging_mfc"]
                calmdown_mfc = dict_line["calmdown_mfc"]

                break
        except:
            pass
    handle.close()

    return spectrum_filename,amount_of_scans, valve_position, purging_time, calmdown_time, purging_mfc, calmdown_mfc



def MakeScan(filename,valve_number,amount_of_scans,purging_time, calmdown_time, purging_mfc, calmdown_mfc):
    #signal.signal(signal.SIGALRM, TimeoutHandler())
    #global interrupted
    critical_errors = False


    try:
        servo_motor.switch_valve_position(valve_number)
        lg.MakeLogEntry(f"Multi inlet valved switched to position {valve_number}")
    except:
        critical_errors = True
        #interrupted = True
        lg.MakeLogEntry(f"Sampling terminated as multi inlet valve is not responding")

    if not critical_errors:
        try:
            for i in range(3):
                VSC_comms.ChangeMFCMode("Open")
                VSC_comms.LogVSCData()
                time.sleep(10)
                VSC_comms.ChangeMFCFlowRate("Close")
                time.sleep(15)
            time.sleep(40)
            VSC_comms.LogVSCData()

            
        except:
            critical_errors = True
            lg.MakeLogEntry(f"Sampling failed due to purging error")

        if not critical_errors:


                lg.MakeLogEntry(f"Purge finalized")

                for i in range(amount_of_scans):
                    try:
                        spectrum_to_analyze, intital_mass, step, ErrorMessage = RGA_comms.AppendSpectrumJSON(filename)

                        if (ErrorMessage != None) and (ErrorMessage != "TIMEOUT") and (not ("Failed to create measurement" in str(ErrorMessage))) and (not ("LinkDown" in ErrorMessage)):
                            critical_errors = True
                            lg.MakeLogEntry(f"Sampling terminated due to RGA error: {ErrorMessage}")
                            break


                        elif ErrorMessage != None:
                            if "Failed to create measurement" in str(ErrorMessage):
                                lg.MakeLogEntry(f"Sampling failed due to 500: Failed To Create Measurement error; repeating attempt")
                            if "LinkDown" in str(ErrorMessage):
                                lg.MakeLogEntry(f"Sampling failed due to LinkDown Serial error; repeating attempt")
                            if str(ErrorMessage) == "TIMEOUT":
                                lg.MakeLogEntry(f"Sampling failed due to TIMEOUT error (probable packet loss); repeating attempt")




                        else:


                            if valve_number != 16:
                                try:
                                    if_abnormalities, void = ar.AnalyseSingleLine(spectrum_to_analyze,valve_number,intital_mass,step,filename)
                                    if if_abnormalities:
                                        Logging.MakeLogEntry(f"Abnormal readings were found for Filename = {filename} scan. Check AbnormalityLog for details")
                                except:
                                    lg.MakeLogEntry(f"Abnormality scan for Filename = {filename} crashed with error")
                            else:
                                if_abnormalities = False




                    except:
                        critical_errors = True
                        #interrupted = True
                        lg.MakeLogEntry(f"Sampling terminated due to unknown RGA error")
                        break





                    try:
                        VSC_comms.LogVSCData("MainConfig")
                    except:
                        Logging.MakeLogEntry("Failed to log VSC data")

                    try:
                        ArduinoComms.LogArduinoData()
                    except:
                        Logging.MakeLogEntry("Failed to reach Arduino board for recording temperature and pressure")

                    time.sleep(10)

                return critical_errors



def DoTask(config="MainConfig"):
    taskname = GetTask(config)
    lg.MakeLogEntry(f"Task {taskname} initiated")

    handle = open("__currenttaskname__","w")
    handle.write(taskname)
    handle.close()

    spectrum_filename, amount_of_scans, valve_position, purging_time, calmdown_time, purging_mfc, calmdown_mfc = GetTaskData(taskname,config)
    critical_errors = MakeScan(spectrum_filename, valve_position, amount_of_scans, purging_time, calmdown_time, purging_mfc, calmdown_mfc)

    os.system("rm __currenttaskname__")

    if not critical_errors:
        lg.MakeLogEntry(f"Task {taskname} finished without errors\n")
    else:
        lg.MakeLogEntry(f"Task {taskname} finished with error\n")

        NotifyUser("Sampling terminated due to error",True)





    return critical_errors



