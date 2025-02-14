import json
import datetime
import JSONoperators as js



def MakeLogEntry(message,config="MainConfig",log_name=None):  #function to make log entry
    if log_name == None:
        log_name = js.ReadJSONConfig("log","MainLog","MainConfig")
    js.assert_file_exists(log_name)
    handle = open(log_name,"a")
    handle.write("\n")

    handle.write(f"{datetime.datetime.now()}: {message}")
    handle.close()


#MakeLogEntry("test!")