#finds the guids of all the files

import json
import os
guids={}
from unityparser import UnityDocument

import helper


projectDirectory = "/media/ramiro/DATA/User/Desktop/InMotion/Inmotion--Jogo/InMotion_GameFiles/Assets"
excludedDirectories = ["Library","UniGLTF","Assets\\Orbbec\\Scripts"]

paths, files =  helper.getFiles(projectDirectory,ext=".meta",excludedDirectories=excludedDirectories)

for p, f in zip(paths,files):
    doc = UnityDocument.load_yaml(os.path.join(p , f))
    guids[doc.entry["guid"]] = (p,f[0:len(f)-len(".meta")])

with open("guids.json","w") as f:
    json.dump(guids,f)
print("Done!")