#getsallstarter nodes, only needs to be run after scripts are added to the scene

import os
import helper
import time
import json
fileextension=".unity"

excludedDirectories = ["Library","UniGLTF","Assets\\Orbbec\\Scripts"]

projectDirectory = "/media/ramiro/DATA/User/Desktop/InMotion/Inmotion--Jogo/InMotion_GameFiles/Assets"

#paths, files = helper.getFiles(projectDirectory,fileextension,remove_extension=False)

with open("guids.json","r")as f:
    guids = json.load(f)
with open("foundguids.json","r")as f:
    foundguids = json.load(f)



actualobjectsguids =[]


def GetScripts(guid,analised):

    scripts=[]

    for guid in foundguids[key]:
        #checks again keys of guids if it is valid
        if guid in guids and guid not in analised:
            analised.append(guid)

            #check if is valid file
            if guids[guid][1].endswith(".prefab") or guids[guid][1].endswith(".asset"):
                
                extractedguids = helper.guidsInFileBruteParsing(os.path.join(guids[guid][0],guids[guid][1]))
                analisedtoadd , scriptstoadd =GetScripts(extractedguids,analised)

                analised=analised + analisedtoadd
                scripts = scripts + scriptstoadd


            if guids[guid][1].endswith(".cs"):
                scripts.append(guids[guid][1])

    return analised, scripts


allstarts={}    

#fir the guids of each scene
for key in foundguids.keys():

    print(key)
    analised=[]

    #iterate all
    analised, scripts = GetScripts(foundguids[key],analised)

    print(scripts)

    scriptsname =[]
    for script in scripts:
        scriptsname.append(script[0:len(script)-len(".cs")])

    allstarts[key]=scriptsname

    

    with open("starternodes.json","w") as f:
        json.dump(allstarts,f)
        





