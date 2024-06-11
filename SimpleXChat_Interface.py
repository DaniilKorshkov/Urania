import json
import os
import subprocess
import sys


#JSONConfigFilename = 'MainConfig'
def GetUsername(JSONConfigFilename):
    handle = open(JSONConfigFilename,'r')
    for line in handle:
        interpreted_line = json.loads(line)
        if interpreted_line["class"] == "simplex-username":
            Username = interpreted_line["username"]
            break
    return Username

def SendCommandToUser(Message,JSONConfigFilename='MainConfig'):
    Username = GetUsername(JSONConfigFilename)
    simplex = subprocess.Popen("simplex-chat",stdin=PIPE)#, input=bytes(f"@{Username} {Message}",'ascii'))
    simplex.stdin(f"@{Username} {Message}")
    #subprocess.(f"@{Username} {Message}")


SendCommandToUser("Hello")