import json
import datetime
import JSONoperators as js



def MakeLogEntry(message,config="MainConfig"):  #function to make log entry
    log_name = js.ReadJSONConfig("log","MainLog","MainConfig")
    js.assert_file_exists(log_name)
    handle = open(log_name,"a")
    handle.write("\n")

    handle.write(f"{datetime.datetime.now()}: {message}")
    handle.close()


#MakeLogEntry("test!")