#generates full dependencies graph, in dots and pdf

import os
import datetime
import helper
import pygraphviz as pgv
import Flags



timenow = datetime.datetime.now().strftime("%H_%M_%S")

def SaveGraph2(graph,path,name,layout="dot"):

    if os.path.exists("output/graph%s"%timenow) == False:
        os.mkdir("output/graph%s"%timenow) 

    graph.write('output/graph%s/%s.dot' % (timenow,name))
    graph.layout(layout)
    graph.draw('output/graph%s/%s.pdf' % (timenow,name))



def SaveGraph(graph,name,layout="sfdp"):
    graph.write('output/graph%s-%s.dot' % (datetime.datetime.now().strftime("%H_%M_%S"),name))
    graph.layout(layout)
    graph.draw('output/graph%s-%s.pdf' % (datetime.datetime.now().strftime("%H_%M_%S"),name))

    print("Saved in:",'output/graph%s-%s.dot' % (datetime.datetime.now().strftime("%H_%M_%S"),name) )






def bfs(graph,node, depth):
    
    myneibs = [node] 
    print("wow")
    print(myneibs)
    if depth<2:
        return myneibs

    myneibs=graph.neighbors(node)

    for neib in graph.neighbors(node):
    
        myneibs = myneibs + bfs(graph,neib,depth-1)

    
    return myneibs 

def remove_duplicates(x):
  return list(dict.fromkeys(x))

def updateNode(name, attrs):

    n = g.get_node(name)[0]

    for key in attrs.keys():

        method_to_call = getattr(n, 'set_%s'%key)
        result = method_to_call(attrs[key])
    g.add_node(n)


def clearcomments(data):

    return data

def parsedata(data):

    dataaux = data.replace('.',' . ')
    dataaux = dataaux.replace('=',' = ')
    dataaux = dataaux.replace(')',' ) ')
    dataaux = dataaux.replace('<',' < ')
    dataaux = dataaux.replace('>',' > ')
    dataaux = dataaux.replace(';',' ; ')       
        
    dataaux = dataaux.split(' ')

    return dataaux

def main():
    edgecounter=0

    flags = Flags.Flags()

    counts={}


    fileextension=".cs"

    projectDirectory = "/media/ramiro/DATA/User/Desktop/InMotion/Inmotion--Jogo/InMotion_GameFiles/Assets"

    excludedDirectories = ["Library","UniGLTF","Assets\\Orbbec\\Scripts"]
    G=pgv.AGraph(strict=False,directed=True)

    #timenow= datetime.datetime.now().strftime("%H_%M_%S")
    allTheFiles, allTheNames = helper.getFiles(projectDirectory,ext=fileextension,excludedDirectories=excludedDirectories,remove_extension=True)
    print("%d files found" % len(allTheFiles))
  

    for fullpath, name in zip(allTheFiles,allTheNames):

        #print(name)

        with open(fullpath,encoding="latin-1") as file:

            data = file.read() 
            
            #put into array
            dataarr = helper.parsedata(data)

            nodeedges=0

            G.add_node(name,shape="box")

            flags.reset()

            parents =  []
            
            counts={}


            #if (name == "OverallManager"):
            #    print(dataarr)


            for i in range(len(dataarr)-1):
                

                

                flags.detector(dataarr[i],dataarr[i+1])                       
            
                #find any references to other scripts
                if dataarr[i] in allTheNames:
                    
                    #createcount if donest exist
                    if dataarr[i] not in counts:
                        counts[dataarr[i]] = 0

                    

                    if flags.inlinecomment==False and flags.multilinecomment == False and flags.string==False:
                        counts[dataarr[i]] = counts[dataarr[i]] + 1
                    
                        if dataarr[i] == name:
                            counts[dataarr[i]] = counts[dataarr[i]] - 1

                        if flags.inheritance==True:
                            #print(counts[dataarr[i]])
                            parents.append(dataarr[i])

                    #uncount if is not in constructor 



                    if dataarr[i+1]=="(" and flags.constructor==False:
                        counts[dataarr[i]] = counts[dataarr[i]] -1
                    
                #dont count and change color if it is static instance
                if data.find("public static %s instance" % dataarr[i])>-1:
                    G.get_node(name).attr['color']= "blue"
                    counts[dataarr[i]] = counts[dataarr[i]] -1

            #print(name,parents)
            for k in counts:
                
                
                if counts[k] > 0:

                    # and we obviosuly need to add the edge to our graph
                    G.add_edge(name,k,weight=counts[k])

                    #set parent relation
                    if k in parents:

                        G.get_edge(name,k).attr['color']="yellow"
            
            #check if is static
            if data.find("public static class %s" % name)>-1:
                G.get_node(name).attr['color']= "green"  

            edgecounter=edgecounter+nodeedges

    print(edgecounter)
    print("There are %d edges" % G.number_of_edges())

    G.graph_attr['ranksep']="5.0"
    G.graph_attr['nodesep']="0.25"
    #G.graph_attr['shape']="box"
    #G.graph_attr['newrank']="true"
    G.graph_attr['concentrate']="false"
    SaveGraph(G,"normal","dot")





if __name__ == "__main__":
    main()