import JSONoperators
from TaskManagement import DoTask
import signal
import os
import SystemCheck
import JSONoperators
import tracemalloc


def signal_handler(signal, frame):
        global interrupted
        interrupted = True
        print(f"Interruption request received. Sampling will be terminated soon")


def Sampling():


        global interrupted
        interrupted = False
        signal.signal(signal.SIGINT, signal_handler)

        JSONoperators.MergeJSONConfigs("MainConfig","DefaultMainConfig")


        failures_found = SystemCheck.SystemCheck("MainConfig")
        #failures_found = False

        if not failures_found:

                handle = open(".VSCINUSE", 'w')
                handle.close()

                tracemalloc.start()


                while True:
                        DoTask()


                        if interrupted:

                                snapshot = tracemalloc.take_snapshot()
                                statistics = snapshot.statistics('lineno')

                                print("results:")
                                for stat in statistics[:10]:
                                        print(stat)


                                print(f"Sampling process terminated")
                                os.system("rm .VSCINUSE")
                                break
        else:
                print("Faliures found")


Sampling()