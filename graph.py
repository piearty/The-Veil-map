# this file does the graph writing and processing using networkx and graphviz
# right now it's very specialized to work for making relationship maps for The Veil prg campaign I'm in
# (i'm a huge nerd)

# graph maker
import networkx as nx
# converts graph to .dot file to be written by graphviz
from networkx.drawing.nx_pydot import to_pydot, write_dot
import pydot

# random in order to create unique keys
import random

# defines a directed multigraph called 'The Veil':
# a graph that can have multiple lines between two nodes, and has arrows
g = nx.MultiDiGraph(label="The Veil")

# colors for the emotional states. 
# these are dictionaries so that the add_edges_from networkx function can read them properly
colors = {'blue':'#002ba1', 'yellow':'#f6e53d', 'green':'#438718', 'red':'#a90f0f', 'purple':'#954ed2', 'orange':'#ea8218'}

# states and obligationColors that are linked to the aforementioned colors
# they are dictionaries so i can reference their names instead of the color when using attributes. like states[sad] instead of colors[blue]
# subject to change as this gets more general
states = {'sad':{'color':colors['blue']}, 'joyful':{'color':colors['yellow']}, 'scared':{'color':colors['green']}, 'angry':{'color':colors['red']}, 'powerful':{'color':colors['purple']}, 'peaceful':{'color':colors['orange']}}
obligationColors = {'sad':{'fontcolor':colors['blue']}, 'joyful':{'fontcolor':colors['yellow']}, 'scared':{'fontcolor':colors['green']}, 'angry':{'fontcolor':colors['red']}, 'powerful':{'fontcolor':colors['purple']}, 'peaceful':{'fontcolor':colors['orange']}}
# determines arrowhead style (whether it's an arrow or an empty dot)
# indicates whether the emotion is felt about someone or for someone's sake
# "i am mad at you" = arrow
# "i am scared for your sake" = dot
tenors = {'for':{'arrowhead':'odot'}, 'toward':{'arrowhead':'normal'}}
# determines edge (line) style (whether it's dotted or a bold line)
# indicates how strong relationship is
# tenuous/not fully formed = dotted
# strong = bold
strength = {'tenuous':{'style':'dotted'}, 'strong':{'style':'bold'}}

# a class that creates objects that can be used to make edges with the add_edges_from function
# attributes are all attributes that the edge will have
class Connection:
    def __init__(self, source, target, state, key, obligation=None, tenor=None, line='strong'):
        self.source = source
        self.target = target
        self.state = state
        self.key = key
        self.obligation = obligation
        self.tenor = tenor
        self.line = line

    #  puts attributes in a dictionary to be read as needed
    def to_dict(self):
        return dict(
            # instance attributes only
            [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]
        )




key_list = []

def uniqueKey():
    singleKey = random.getrandbits(20)
    if singleKey not in key_list:
        key_list.append(singleKey)
        return singleKey

RibbonCalder = Connection('Ribbon', 'Calder', 'joyful', uniqueKey())
RibbonCalder2 = Connection('Ribbon', 'Calder', 'peaceful', uniqueKey())
RibbonThiago = Connection('Ribbon', 'Thiago', 'peaceful', uniqueKey())

# turns object attributes into a list that can be readable by add_edges_from
def listConnection(singleConnection):
    # list to contain connection attributes
    connectionList = [singleConnection.source, singleConnection.target, 'key=' + str(singleConnection.key)]
    # calls the .to_dict() method in the singleConnection object and saves dictionary in connectDict
    connectDict = singleConnection.to_dict()
    # for attribute key in connectDict
    for attribute in connectDict:
        # if it's not already in there
         # merges attribute to attributes dictionary according to attribute
        if connectDict[attribute] and attribute not in ('source', 'target'):            
            if attribute is 'state':
                connectionList.append(states[singleConnection.state])
            elif attribute is 'obligation':
                connectionList.append({'label':singleConnection.obligation})
                connectionList.append(obligationColors[singleConnection.state])
            elif attribute is 'tenor':
                connectionList.append(tenors[singleConnection.tenor])
            elif attribute is 'line':
                connectionList.append(strength[singleConnection.line])
    return connectionList

# function to shorten typing bc i'm lazy
# uses add_edges_from to create an edge
def addEdge(singleConnection):
    g.add_edge(*listConnection(singleConnection))

# function to remove given edge
def removeEdge(singleConnection):
    connectionAsList = listConnection(singleConnection)
    #unpacks and removes given edge
    g.remove_edge(*connectionAsList[:3])
    if len(nx.algorithms.descendants(g, connectionAsList[0])) == 0:
        g.remove_node(connectionAsList[0])
    if len(nx.algorithms.descendants(g, connectionAsList[1])) == 0:
        g.remove_node(connectionAsList[1])


print(*listConnection(RibbonCalder)[2:3])
print(*listConnection(RibbonCalder2)[:3])
addEdge(RibbonCalder)
addEdge(RibbonCalder2)
#addEdge(RibbonThiago)

#print(nx.algorithms.descendants(g, listConnection(RibbonCalder)[0]))
print(g.edges())
removeEdge(RibbonCalder2)

print(g.edges())

#print(g, listConnection(RibbonCalder)[0])

p = to_pydot(g)
p.write_dot('test.dot')
p.write_png('test.png', prog='dot')