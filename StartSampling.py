from TaskManagement import DoTask
import signal
import os

def signal_handler(signal, frame):
        global interrupted
        interrupted = True
        print(f"Interruption request received. Sampling will be terminated soon")


def Sampling():


        global interrupted
        interrupted = False
        signal.signal(signal.SIGINT, signal_handler)



        handle = open(".VSCINUSE", 'w')
        handle.close()


        while True:
                DoTask()


                if interrupted:
                        print(f"Sampling process terminated")
                        os.system("rm .VSCINUSE")
                        break



Sampling()