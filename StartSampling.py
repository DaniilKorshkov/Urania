from TaskManagement import DoTask
import signal
import os

def signal_handler(signal, frame):
        global interrupted
        interrupted = True


def Sampling():


        global interrupted
        interrupted = False
        signal.signal(signal.SIGINT, signal_handler)



        handle = open(".VSCINUSE", 'w')
        handle.close()


        while True:
                DoTask()


                if interrupted:
                        print("Exiting sampling program")
                        os.system("rm .VSCINUSE")
                        break



Sampling()