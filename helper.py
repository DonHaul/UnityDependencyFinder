import os
import json

def parsedata(data, characters=['.','=',')','(','<','<',';',',','{','}','+','-','/','*','%','\n','&&','||','\"','\'']):

    dataaux = data

    for c in characters:

        dataaux = dataaux.replace(c,' %s '% c)      
        
    dataaux = dataaux.split(' ')

    #filter out empties
    return list(filter(lambda a:a!='',dataaux))

def guidsInFileBruteParsing(filepath):


    guids=[]

    with open(filepath,"r",encoding="latin-1") as f:
        data=f.read()
        
        data = parsedata(data,[':',','])

        guidIds = [i for i,x in enumerate(data) if x == "guid"]
        with open("lol.txt",'w') as g:
            json.dump(data,g)

        for ids in guidIds:
            guids.append(data[ids+1])

    return guids


def getFiles(dir,ext=".cs",excludedDirectories=[],remove_extension=False):
    allFiless=[]
    allNames = []
    #goes trhoug all files
    for path, subdirs, files in os.walk(dir):
        for name in files:

            if name.endswith(ext):
                
                inExcluded = False

                for excluded in excludedDirectories:
                    if excluded in path:

                        inExcluded = True

                if not inExcluded:
                    allFiless.append(os.path.join(path,name))
                    #print(os.path.join(path, name))

                    #removes extension
                    if remove_extension:
                            name = name[0:len(name)-len(ext)]

                    allNames.append(name)


    return allFiless, allNames