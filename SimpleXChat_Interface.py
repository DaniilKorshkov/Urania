import json


import os
import subprocess
import sys
import time
import pythonmonkey
import websocket
from websockets.sync.client import connect
import pyautogui as pg


#JSONConfigFilename = 'MainConfig'
def GetUsername(JSONConfigFilename):
    handle = open(JSONConfigFilename,'r')
    for line in handle:
        interpreted_line = json.loads(line)
        if interpreted_line["class"] == "simplex-username":
            Username = interpreted_line["username"]
            break
    return Username

def SendCommandToUser(Message,ConfigName = 'MainConfig'):

    ClientName = GetUsername(ConfigName)

    '''
    pg.hotkey("ctrl","alt","t")
    time.sleep(1)
    pg.typewrite("simplex-chat")
    pg.press('enter')
    time.sleep(2.5)
    pg.typewrite(f"@{ClientName} {Message}")
    time.sleep(1)
    pg.press("enter")
    time.sleep(0.5)
    pg.typewrite("/quit")
    pg.press("enter")
    time.sleep(0.5)
    pg.typewrite("exit")
    pg.press("enter")'''


    os.system(f'simplex-chat -e "@{ClientName} {Message}"')


def SendCommandWithSubprocess():
    simplex = subprocess.Popen("simplex-chat", stdin=subprocess.PIPE)  # , input=bytes(f"@{Username} {Message}",'ascii'))
    #simplex.stdin(f"@UraniaClient Hello")
    # subprocess.(f"@{Username} {Message}")

SendCommandWithSubprocess()

#SendCommandToUser('123aaa')