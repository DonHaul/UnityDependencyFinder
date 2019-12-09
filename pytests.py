import os


import matplotlib.pyplot as plt
import datetime


import pydot

g = pydot.Dot()
g.set_node_defaults(color='lightgray', style='filled', shape='box',fontname='Courier', fontsize='10')


edge = pydot.Edge("ola","me2")
g.add_edge(edge)
edge = pydot.Edge("ola","me2")
g.add_edge(edge)
edge = pydot.Edge("ola","me2")
g.add_edge(edge)
edge = pydot.Edge("ola","me2")
g.add_edge(edge)
edge = pydot.Edge("ola","me2")
g.add_edge(edge)
edge = pydot.Edge("ola","me2")
g.add_edge(edge)
edge = pydot.Edge("ola","me2")
g.add_edge(edge)


g.add_node(pydot.Node("ola",color="red"))
# and we obviosuly need to add the edge to our graph
g.add_edge(edge)
                


g.write('output/graph%s.txt' % datetime.datetime.now().strftime("%H_%M_%S"))


g.write_png('output/graph%s.png' % datetime.datetime.now().strftime("%H_%M_%S"))


