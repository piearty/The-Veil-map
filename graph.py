#graph maker
import networkx as nx
#converts graph to .dot file to be written by graphviz
from networkx.drawing.nx_pydot import write_dot
import pydot

g = nx.MultiDiGraph(label="The Veil")

colors = {'blue':'#545b90', 'yellow':'#fbfd54', 'green':'#438718', 'red':'#a90f0f', 'purple':'#954ed2', 'orange':'#ea8218'}

emotions = {'sad':{'color':colors['blue']}, 'joyful':{'color':colors['yellow']}, 'scared':{'color':colors['green']}, 'angry':{'color':colors['red']}, 'powerful':{'color':colors['purple']}, 'peaceful':{'color':colors['orange']}}
labelColors = {'sadLabel':{'fontcolor':colors['blue']}, 'joyfulLabel':{'fontcolor':colors['yellow']}, 'scaredLabel':{'fontcolor':colors['green']}, 'angryLabel':{'fontcolor':colors['red']}, 'powerfulLabel':{'fontcolor':colors['purple']}, 'peacefulLabel':{'fontcolor':colors['orange']}}
isFor = {'arrowhead':'odot'}
strength = {'tenuous':{'style':'dotted'}, 'strong':{'style':'bold'}}


class Connection:
    def __init__(self, source, target, state, label=None, fontcolor=None, arrow=None, line=strength['strong']):
        self.source = source
        self.target = target
        self.state = state
        self.label = label
        self.fontcolor = fontcolor
        self.arrow = arrow
        self.line = line


    def to_dict(self):
        return dict(
            [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]
        )

RibbonCalder = Connection('Ribbon', 'Calder', 'peaceful', {'label':'2'}, labelColors['peacefulLabel'])
CalderRibbon = Connection('Calder', 'Ribbon', 'scared', isFor)
RibbonAliquot = Connection('Ribbon', 'Aliquot', 'peaceful', {'label':'1'}, labelColors['peacefulLabel'])

def listConnection(singleConnection):
    names = [singleConnection.source, singleConnection.target]
    attributes = {}
    attributes.update(emotions[singleConnection.state])
    connectDict = singleConnection.to_dict()
    for attribute in connectDict:
        if connectDict[attribute] and attribute not in ('source', 'target', 'state'):
            print(connectDict[attribute])
            attributes.update(connectDict[attribute])
    names.append(attributes)
    return names

def addEdge(singleConnection):
    g.add_edges_from([listConnection(singleConnection)])


#addEdge(RibbonCalder)
addEdge(CalderRibbon)
#addEdge(RibbonAliquot)

graphdot = write_dot(g,'multi.dot')