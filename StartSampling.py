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
        Logging.MakeLogEntry("Sampling initiated by user")


        try:
                RGA.change_rga_ip("MainConfig")
                RGA_working = True
        except:
                RGA_working = False
                Logging.MakeLogEntry("Failed to reach RGA. Sampling is cancelled\n")

        if RGA_working:
                failures_found = SystemCheck.SystemCheck("MainConfig")
        else:
                failures_found = True

        #failures_found = False

        if not failures_found:

                handle = open(".VSCINUSE", 'w')
                handle.close()

                tracemalloc.start()


                while True:
                        critical_errors = DoTask()
                        if critical_errors:
                                interrupted = True



                        if interrupted:

                                snapshot = tracemalloc.take_snapshot()
                                statistics = snapshot.statistics('lineno')

                                print("results:")
                                for stat in statistics[:10]:
                                        print(stat)


                                print(f"Sampling process terminated")
                                os.system("rm .VSCINUSE")
                                if not critical_errors:
                                        Logging.MakeLogEntry("Sampling terminated by user\n")
                                        break
                                else:
                                        Logging.MakeLogEntry("Sampling terminated due to error\n")

                                        try:
                                                ret = str((subprocess.run(["pwd"], capture_output=True)).stdout)

                                                ret = ret.strip("b")
                                                ret = ret.strip("'")
                                                ret = ret.strip("\\n")

                                                os.system(f'notify-send -u critical -i {ret}/ErrorIcon.png "Sampling terminated due to error"')
                                        except:

                                                os.system(f'notify-send -u critical "Sampling terminated due to error"')


                                        break


        else:
                print(f"Failures found")
                #Logging.MakeLogEntry("Sampling terminated by user due to SystemCheck recommendation")



Sampling()