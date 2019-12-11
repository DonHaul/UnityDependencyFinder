#grabs found scrips for each scene, and based on total graph, generates each scene subgraph

import os
import pygraphviz as pgv
import json
import depFinder
with open("starternodes.json",'r') as f:
    data = json.load(f)


def GrowGraph(nbunch,G,analized=[]):

    toanalizenext=[]


    for n in nbunch:

        if n in analized:
            #no nodes to analise next
            return [],analized
        else:
                       
            #analized them and get next to analyse
            analized.append(n)
            nodes  = G.out_neighbors(n)

            #if the next to analise are not already analysed
            for nnn in nodes:
                if nnn not in analized:
                    toanalizenext.append(nnn)


            #nodes are analized
            toanalizenext,analized = GrowGraph(toanalizenext,G,analized)


    #to analize next, and the already analized
    return toanalizenext,analized
        
G=pgv.AGraph("output/graph01_30_52-normal.dot")  

for k in data:
    nodes=[]
#    print(k)
#k="8 Glass cleaner.unity"
    G.clear()
    G=pgv.AGraph("output/graph01_30_52-normal.dot")  
    
    #grow graph
    _,nodes = GrowGraph(data[k],G,[])

    for n in data[k]:
        G.get_node(n).attr['color']= "red"  

    
    toremove=[]
    for n in G.nodes():
        if n not in nodes:
            toremove.append(n)

    G.remove_nodes_from(toremove)


    

    G.graph_attr['concentrate']="false"

    depFinder.SaveGraph2(G,"",k)

    



print("end")
print(nodes)

quit()

