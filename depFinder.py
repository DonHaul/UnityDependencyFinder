import os

fileextension=".cs"

projectDirectory = "/media/ramiro/DATA/User/Desktop/InMotion/Inmotion--Jogo/InMotion_GameFiles/Assets"

excludedDirectories = ["Library","UniGLTF","Assets\\Orbbec\\Scripts"]

import datetime

import pygraphviz as pgv
G=pgv.AGraph(strict=False,directed=True)

def SaveGraph(graph,name,layout="sfdp"):
    graph.write('output/graph%s-%s.dot' % (datetime.datetime.now().strftime("%H_%M_%S"),name))
    graph.layout(layout)
    graph.draw('output/graph%s-%s.pdf' % (datetime.datetime.now().strftime("%H_%M_%S"),name))

def getFiles(dir):
    allFiless=[]
    allNames = []
    #goes trhoug all files
    for path, subdirs, files in os.walk(dir):
        for name in files:

            if name.endswith(fileextension):
                
                inExcluded = False

                for excluded in excludedDirectories:
                    if excluded in path:

                        inExcluded = True

                if not inExcluded:
                    allFiless.append(os.path.join(path, name))
                    #print(os.path.join(path, name))
                    allNames.append(name[0:len(name)-3])


    return allFiless, allNames

allTheFiles, allTheNames = getFiles(projectDirectory)


print("%d files found" % len(allTheFiles))

#for name in allTheNames:
    
#    g.add_node(pydot.Node(name))

#generate graph

lol=0

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


if "Animercise" in allTheNames:
    print("IT IS THEE")

edgecounter=0
for fullpath, name in zip(allTheFiles,allTheNames):
    with open(fullpath,encoding="latin-1") as file:
        lol=lol+1
        #print(lol)
 
        #print(fullpath) 
        data = file.read() 
        
        dataaux = data.replace('.',' ')
        dataaux = dataaux.replace('=',' ')
        dataaux = dataaux.replace(')',' ')
        dataaux = dataaux.replace('<',' ')
        dataaux = dataaux.replace('>',' ')
        dataaux = dataaux.replace(';',' ')

        
        
        dataarr = dataaux.split()

        nodeedges=0

        G.add_node(name,shape="box")


        #if name=="GameRecnMake":
        #    print(dataarr)
        #    if("Animater" in dataarr):
        #        print("WTFF")


        #find any references to other scripts
        for othername in allTheNames:


            count = dataarr.count(othername)

            hasaway=False

            #dont count if is self
            if name == othername:
                count = count - 1

            #dont count if is parent class
            if data.find(": %s" % othername)>-1:
                #count = count - 1
                hasaway=True

            #font count if is interface
            if data.find(", %s" % othername)>-1:
                #count = count - 1
                hasaway=True
            
            

            #dont count and change color if it is static instance
            if data.find("public static %s instance" % othername)>-1:
                count = count - 1
                G.get_node(name).attr['color']= "blue"  



            #every scripts has alway one ocurrent when defining the class
            if count >0:


                 # and we obviosuly need to add the edge to our graph
                G.add_edge(name,othername,weight=count)

                if hasaway:
                    G.get_edge(name,othername).attr['color']="yellow"
                
                nodeedges=nodeedges+count

        
        #check if is static
        if data.find("public static class %s" % name)>-1:
            G.get_node(name).attr['color']= "green"  

        edgecounter=edgecounter+nodeedges

print(edgecounter)
print("There are %d edges" % G.number_of_edges())

#remove double edges
#for edge in G.edges_iter():
#    #if is double direction, put in one single arrow
#    if G.has_edge(edge[1],edge[0]):
#        
#        G.add_edge(edge[1],edge[0],"double",dir="both")
#        G.remove_edge(edge[0],edge[1])


#remove lonely
#for deg,node in zip(G.degree(),G.nodes()):
#    if deg==0:
#        G.remove_node(node)

#adapt samehead and sametail according to rank
        

print("There are %d nodes" % G.number_of_nodes())
print("There are %d edges" % G.number_of_edges())


G.graph_attr['ranksep']="5.0"
G.graph_attr['nodesep']="0.25"
#G.graph_attr['shape']="box"
#G.graph_attr['newrank']="true"
G.graph_attr['concentrate']="true"
SaveGraph(G,"normal","dot")

n= bfs(G,"OverallManager",3)

n=remove_duplicates(n)
Sub =pgv.AGraph(strict=False,directed=True)
Sub.add_nodes_from(n)
Sub.add_edges_from(G.edges(n))
Sub.graph_attr['ranksep']="5.0"
Sub.graph_attr['nodesep']="0.25"

SaveGraph(Sub,"sub","dot")
print("There are %d nodes" % Sub.number_of_nodes())




