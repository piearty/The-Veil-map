# this file does the graph writing and processing using networkx and graphviz
# right now it's very specialized to work for making relationship maps for The Veil prg campaign I'm in
# (i'm a huge nerd)

# graph maker
import networkx as nx
# converts graph to .dot file to be written by graphviz
from networkx.drawing.nx_pydot import to_pydot, write_dot, read_dot
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



# takes a dot file and opens it, turning it into a 
def open_dot(dotFile):
    openedFile = read_dot(dotFile)
    return openedFile

# list to hold keys
keys_list = []

# makes unique keys to reference the edges with
def unique_key():
    # makes a key
    singleKey = random.getrandbits(20)
    # checks if key is not already in key_list and if isn't put it in keys_List and return it
    # basically makes sure keys are unique
    if singleKey not in keys_list:
        keys_list.append(singleKey)
        return singleKey

RibbonCalder = Connection('Ribbon', 'Calder', 'joyful', unique_key())
RibbonCalder2 = Connection('Ribbon', 'Calder', 'peaceful', unique_key())
RibbonThiago = Connection('Ribbon', 'Thiago', 'peaceful', unique_key())

# turns object attributes into a list that can be readable by add_edges_from
def list_connection(singleConnection):
    # initial list ['Ribbon', 'Calder', a unique ID number]
    names = [singleConnection.source, singleConnection.target, 'key=' + str(singleConnection.key)]
    # an empty dictionary
    attributes = {}
    connectDict = singleConnection.to_dict()
    # for attribute key in connectDict
    for attribute in connectDict:
        # if it's not already in there
         # merges attribute to attributes dictionary according to attribute
        if connectDict[attribute] and attribute not in ('source', 'target'):            
            if attribute is 'state':
                attributes.update(states[singleConnection.state])
            elif attribute is 'obligation':
                attributes.update({'label':singleConnection.obligation})
                attributes.update(obligationColors[singleConnection.state])
            elif attribute is 'tenor':
                attributes.update(tenors[singleConnection.tenor])
            elif attribute is 'line':
                attributes.update(strength[singleConnection.line])

    names.append(attributes)
    return names

# function to shorten typing bc i'm lazy
# uses add_edges_from to create an edge
def add_edge(singleConnection):
    g.add_edges_from([list_connection(singleConnection)])

# function to remove given edge
# this doesn't quite work yet, deletes all edges associated :(
def remove_edge(singleConnection):
    connectionAsList = list_connection(singleConnection)
    #unpacks and removes given edge
    g.remove_edge(*connectionAsList[:3])
    # if nodes that edge was connected to doesn't have any remaining connections, delete them
    # for first node
    if len(nx.algorithms.descendants(g, connectionAsList[0])) == 0:
        g.remove_node(connectionAsList[0])
    #  and second node
    if len(nx.algorithms.descendants(g, connectionAsList[1])) == 0:
        g.remove_node(connectionAsList[1])


#print(*list_connection(RibbonCalder)[2:3])
#print(*list_connection(RibbonCalder)[2:3])
#print(*list_connection(RibbonCalder2)[:3])
#add_edge(RibbonCalder)
#add_edge(RibbonCalder2)
# add_edge(RibbonThiago)

#print(nx.algorithms.descendants(g, list_connection(RibbonCalder)[0]))
#print(g.edges())
#remove_edge(RibbonCalder)

#print(g.edges())

#print(g, list_connection(RibbonCalder)[0])

p = to_pydot(g)
p.write_dot('test.dot')
p.write_png('test.png', prog='dot')
