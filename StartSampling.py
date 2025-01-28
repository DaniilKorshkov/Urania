from TaskManagement import DoTask
import atexit
import signal
import os

def exit_handler():
        os.system("rm .VSCINUSE")

def kill_handler(*args):
        os.system("rm .VSCINUSE")

def Sampling():

        atexit.register(exit_handler)
        signal.signal(signal.SIGINT, kill_handler)
        signal.signal(signal.SIGTERM, kill_handler)

        handle = open(".VSCINUSE", 'w')
        handle.close()


        while True:
                DoTask()



Sampling()