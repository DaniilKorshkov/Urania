import json


import os
import subprocess



#JSONConfigFilename = 'MainConfig'
def GetUsername(JSONConfigFilename):
    handle = open(JSONConfigFilename,'r')
    for line in handle:
        interpreted_line = json.loads(line)
        if interpreted_line["class"] == "user_notifications":
            Username = interpreted_line["simplex_username"]
            break
    return Username

def SendMessageToUser(Message,ConfigName = 'MainConfig'):

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



#SendCommandToUser('123aaa')