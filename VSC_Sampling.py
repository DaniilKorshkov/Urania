import JSONoperators
from TaskManagement import DoTask
import signal
import os
import SystemCheck
import JSONoperators
import tracemalloc
import Logging
import RGA_comms as RGA
import subprocess
from EmailNotificationSystem import NotifyUser
from ArduinoComms import FillingActClose
import VSC_comms


def signal_handler(signal, frame):
        global interrupted
        interrupted = True
        print(f"Interruption request received. Sampling will be terminated soon")
        Logging.MakeLogEntry("Termination request received from user")


def Sampling():


        global interrupted
        interrupted = False
        signal.signal(signal.SIGINT, signal_handler)


        JSONoperators.MergeJSONConfigs("MainConfig","DefaultMainConfig")
        Logging.MakeLogEntry("VSC sampling initiated by user")


        

        

        

        handle = open(".VSCINUSE", 'w')
        handle.close()

        #tracemalloc.start()


        while True:

                try:
                    VSC_comms.LogVSCData("MainConfig")
                except:
                    NotifyUser("0007", f"VSC Communication/Control Failure (0007)", False)
                    Logging.MakeLogEntry("Failed to log VSC data")





                if interrupted:

                        print(f"VSC sampling process terminated")
                        os.system("rm .VSCINUSE")

                        if not critical_errors:
                                Logging.MakeLogEntry("VSC sampling terminated by user\n")
                                NotifyUser("0016","VSC sampling terminated by user (0016)",False)


                        else:
                                Logging.MakeLogEntry("Sampling terminated due to error\n")

                                
                        try:
                                FillingActClose()
                        except:
                                NotifyUser("0011", f"Arduino actuator control failure (Event 0011)", True)

                        break






        

if __name__ == "__main__":
    Sampling()