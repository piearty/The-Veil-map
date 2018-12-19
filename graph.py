#this file does the graph writing and processing using networkx and graphviz
#right now it's very specialized to work for making relationship maps for The Veil prg campaign I'm in
#(i'm a huge nerd)

#graph maker
import networkx as nx
#converts graph to .dot file to be written by graphviz
from networkx.drawing.nx_pydot import to_pydot, write_dot
import pydot

#defines a directed multigraph called 'The Veil':
#a graph that can have multiple lines between two nodes, and has arrows
g = nx.MultiDiGraph(label="The Veil")

#colors for the emotional states. 
#these are dictionaries so that the add_edges_from networkx function can read them properly
colors = {'blue':'#545b90', 'yellow':'#f6e53d', 'green':'#438718', 'red':'#a90f0f', 'purple':'#954ed2', 'orange':'#ea8218'}

#states and obligationColors that are linked to the aforementioned colors
#they are dictionaries so i can reference their names instead of the color when using attributes. like states[sad] instead of colors[blue]
#subject to change as this gets more general
states = {'sad':{'color':colors['blue']}, 'joyful':{'color':colors['yellow']}, 'scared':{'color':colors['green']}, 'angry':{'color':colors['red']}, 'powerful':{'color':colors['purple']}, 'peaceful':{'color':colors['orange']}}
obligationColors = {'sad':{'fontcolor':colors['blue']}, 'joyful':{'fontcolor':colors['yellow']}, 'scared':{'fontcolor':colors['green']}, 'angry':{'fontcolor':colors['red']}, 'powerful':{'fontcolor':colors['purple']}, 'peaceful':{'fontcolor':colors['orange']}}
#determines arrowhead style (whether it's an arrow or an empty dot)
#indicates whether the emotion is felt about someone or for someone's sake
#"i am mad at you" = arrow
#"i am scared for your sake" = dot
tenors = {'for':{'arrowhead':'odot'}, 'toward':{'arrowhead':'normal'}}
#determines edge (line) style (whether it's dotted or a bold line)
#indicates how strong relationship is
#tenuous/not fully formed = dotted
#strong = bold
strength = {'tenuous':{'style':'dotted'}, 'strong':{'style':'bold'}}

#a class that creates objects that can be used to make edges with the add_edges_from function
#attributes are all attributes that the edge will have
class Connection:
    def __init__(self, source, target, state, obligation=None, tenor=None, line='strong'):
        self.source = source
        self.target = target
        self.state = state
        self.obligation = obligation
        self.tenor = tenor
        self.line = line

    # puts attributes in a dictionary to be read as needed
    def to_dict(self):
        return dict(
            #instance attributes only
            [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]
        )

RibbonCalder = Connection('Ribbon', 'Calder', 'joyful')

#turns object attributes into a list that can be readable by add_edges_from
def listConnection(singleConnection):
    #initial list ['Ribbon', 'Calder']
    names = [singleConnection.source, singleConnection.target]
    #an empty dictionary
    attributes = {}
    #calls the .to_dict() method in the singleConnection object and saves dictionary in connectDict
    connectDict = singleConnection.to_dict()
    #for attribute key in connectDict
    for attribute in connectDict:
        #if it's not already in there
         #merges attribute to attributes dictionary according to attribute
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

    #adds dictionary to the names list
    #looks like ['Ribbon', 'Calder' {'color': '#ea8218', other attributes}]
    names.append(attributes)
    return names

#function to shorten typing bc i'm lazy
#uses add_edges_from to create an edge
def addEdge(singleConnection):
    g.add_edges_from([listConnection(singleConnection)])

def removeEdge(singleConnection):
    g.remove_edge(*listConnection(singleConnection)[:2])

#turns the graph g into a pydot format
p = to_pydot(g)
p.write_dot('test.dot')
#writes pydot format graph into a png
p.write_png('test.png')