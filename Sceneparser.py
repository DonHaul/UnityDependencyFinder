#will go through all the scene, and using guids, it will finds the scripts in them

import os
import helper
import time
import json
import unityparser
fileextension=".unity"

excludedDirectories = ["Library","UniGLTF","Assets\\Orbbec\\Scripts"]

projectDirectory = "/media/ramiro/DATA/User/Desktop/InMotion/Inmotion--Jogo/InMotion_GameFiles/Assets"

paths, files = helper.getFiles(projectDirectory,fileextension,remove_extension=False)

with open("guids.json","r")as f:
    guids = json.load(f)

#recursive find guids in file
def guidFinder(entry):
    
    guids=[]
    print("Deeper")


    for k in entry:
        #if field is guid add imediatelly
        if k=="guid":
            guids.append(entry[k])

        #if field is ordered dict, iterate it
        if type(entry[k]) == unityparser.constants.OrderedFlowDict:
            guids = guids + guidFinder(entry[k])

        #when is list of params (has the - on the file)
        if type(entry[k])==list:
            for e in entry[k]:
                guids = guids + guidFinder(e)

    return guids

def guidsInFileYAML(filepath):
    guids = []

    doc = unityparser.UnityDocument.load_yaml(filepath)

    #iterate every entry on the yaml file
    for entry in doc.entries:

        #filter out default fields
        fields = [a for a in dir(entry) if a.startswith('m_')]
        
        #iterates  these fileds
        for f in fields:

            attr=getattr(entry, f)
            
            #if one of these fileds is a orderflowdict, iterate it recurssively
            if(type(attr)==unityparser.constants.OrderedFlowDict):
                guids = guids +  guidFinder(attr)

            #if one is a guid, add it immediately
            elif f=="guid":
                guids.append(attr)

    return guids




count=0

allguids={}



for path, fil in zip(paths,files):
    print(os.path.join(path ,fil))
    start= time.time()


    allguids[fil] = helper.guidsInFileBruteParsing(os.path.join(path ,fil))

    #remove duplicates:
    allguids[fil] = list( dict.fromkeys(allguids[fil]) )

    count = count +1

    print("%d/%d"%(count,len(paths)),time.time()-start ,fil)

    

        

with open("foundguids.json","w") as f:
    json.dump(allguids,f)

quit()
