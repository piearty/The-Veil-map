#graph maker
import networkx as nx
#converts graph to .dot file to be written by graphviz
from networkx.drawing.nx_pydot import write_dot
import pydot

g = nx.MultiDiGraph(label="The Veil")

colors = {'blue':'#545b90', 'yellow':'#fbfd54', 'green':'#438718', 'red':'#a90f0f', 'purple':'#954ed2', 'orange':'#ea8218'}

emotions = {'sad':{'color':colors['blue']}, 'joyful':{'color':colors['yellow']}, 'scared':{'color':colors['green']}, 'angry':{'color':colors['red']}, 'powerful':{'color':colors['purple']}, 'peaceful':{'color':colors['orange']}}
labelColors = {'sadLabel':{'fontcolor':colors['blue']}, 'joyfulLabel':{'fontcolor':colors['yellow']}, 'scaredLabel':{'fontcolor':colors['green']}, 'angryLabel':{'fontcolor':colors['red']}, 'powerfulLabel':{'fontcolor':colors['purple']}, 'peacefulLabel':{'fontcolor':colors['orange']}}
toward = {'arrowhead':'odot'}


class Connection:
    def __init__(self, source, target, state, arrow=None, label=None, fontcolor=None):
        self.source = source
        self.target = target
        self.state = state
        self.arrow = arrow
        self.label = label
        self.fontcolor = fontcolor

    def to_dict(self):
        return dict(
            [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]
        )

RibbonCalder = Connection('Ribbon', 'Calder', 'peaceful', None, {'label':'2'}, labelColors['peacefulLabel'])
CalderRibbon = Connection('Calder', 'Ribbon', 'scared', toward)

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

g.add_edges_from([listConnection(RibbonCalder), listConnection(CalderRibbon)])

graphdot = write_dot(g,'multi.dot')