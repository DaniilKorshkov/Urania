import json
import datetime




def GetLogSettings(config="MainConfig"):  #function to get log name from main config
    log_name = None
    handle = open(config, "r")
    for line in handle:
        if line == None or line == "\n":
            continue
        dict_line = json.loads(line)
        if dict_line["class"] == "log":
            log_name = dict_line["MainLog"]
            break
    handle.close()

    if log_name == None:
        raise LookupError("Log filename is not found in main config")
    return log_name

def MakeLogEntry(message,config="MainConfig"):  #function to make log entry
    log_name = GetLogSettings(config)
    handle = open(log_name,"a")
    handle.write("\n\n")

    handle.write(f"{datetime.datetime.now()}: {message}")
    handle.close()


#MakeLogEntry("test!")