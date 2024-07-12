import json
import datetime
import Logging as lg
import JSONoperators as js

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

        if line == "" or line == "\n" or line[0] == "#":
            continue

        dict_line = json.loads(line)
        if dict_line["class"] == "task" and dict_line["type"] == "emergency" and not if_task_found:
            if_task_found = True
            task_to_execute = dict_line["name"]
            try:   # evaluation of executiuon times.
                match dict_line["how_much_executions"]:
                    case "inf":  #infinite executions case
                        text_copy.append(line.strip("\n"))
                    case 1:  #if 1 execution time left, task is no longer executed
                        pass
                    case _:  # else, howmuchexecutions is decremented by 1
                        howmuchexecutions = int(dict_line["how_much_executions"])-1
                        dict_line["how_much_executions"] = howmuchexecutions
                        text_copy.append(json.dumps(dict_line))
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
        dict_line = json.loads(line)
        if dict_line["class"] == "task" and dict_line["type"] == "schedule" and (not if_scheduled_tasks):
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
        dict_line = json.loads(line)
        if dict_line["class"] == "task":
            if dict_line["type"] == "regular":
                if i == current_task_number:
                    task_to_execute = dict_line["name"]
                i += 1
    handle.close()

    UpdateTaskList(tasklist_name, text_copy)

    return task_to_execute



def GetTask(config="MainConfig",do_logging=True):  # function that checks for emergency tasks; for scheduled tasks, for regular tasks and returns name of required task

    tasklist_name = js.ReadJSONConfig("tasks","TaskList")
    default_tasklist_name = js.ReadJSONConfig("tasks","DefaultTaskList")
    js.assert_file_exists(tasklist_name, default_tasklist_name)

    ifemergencytasks, taskname = CheckForEmergencyTasks(config)
    if not ifemergencytasks:
        ifscheduledtasks, taskname = CheckForScheduledTasks(config)
        if not ifscheduledtasks:
            taskname = GetRegularTask(config)

    if do_logging:
        lg.MakeLogEntry(f"{taskname} initiated")

    return taskname

#ret = GetTask()
#print(ret)



