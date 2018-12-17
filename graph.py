import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import pydot
from itertools import product

g = nx.MultiDiGraph(rpg="The Veil")

people = ['Ribbon', 'Calder', 'Thiago', 'Aliquot']
combos = []

for r in product(people, repeat=2):
    if r[0] != r[1]:
        combos.append(r)

print(combos)


g.add_edges_from(combos)

graphdot = write_dot(g,'multi.dot')