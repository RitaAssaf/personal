from pycsp3 import *
import os
import networkx as nx
from pathlib import Path
import pydot


def load(graph_file):
    # Load graph
    graph = nx.drawing.nx_agraph.read_dot(graph_file)

    # Get graph edges and labels
      # Get graph edges and attributes
    edges = graph.edges
    labels = nx.get_node_attributes(graph, 'label')
    angles = nx.get_edge_attributes(graph, 'angle')

    # Extract fields
    NV = graph.number_of_nodes()
    NE = graph.number_of_edges()
    V = [label for label in labels.values()]
    E = [(int(n1), int(n2)) for n1, n2 in edges]
    A = ['c' if angles.get((n1, n2), '0') == '0' else 'l' for n1, n2 in edges]

    return NV, NE, V, E, A


def process_mapping(i):

	# Plot mapping
	graph = pydot.graph_from_dot_file(f'dat/{args.target}.dot')[0]
	for v1 in range(instance['NV_1']):
		graph.get_node(str(mapping[v1]))[0].set_label(instance['V1'][v1])
		graph.get_node(str(mapping[v1]))[0].set_style('filled')
	graph.write_png(f'res/sol_{i}.png')






NV_1, NE_1, V1, E1, O1 = load("pattern.dot")  # pattern graph
NV_2, NE_2, V2, E2, O2= load("target.dot")   # target graph

if NV_1 > 0 and NV_2 > 0:
    # ===== VARIABLES =====
    
    # Map each vertex in the pattern graph to a vertex in the target graph
    I = VarArray(size=NV_1, dom=range(1, NV_2 + 1))
    
    # Precompute undirected edges in the target graph
    undirected_E2 = {(min(x, y), max(x, y)) for x, y in E2}

    # ===== CONSTRAINTS =====
  
    
    satisfy(

		# Map all nodes from graph 1
		AllDifferent(I),

		# Found a mapping from the edge in graph 1 to an edge in graph 2, with angle(e1) = angle(e2)
		# Each edges of graph 1 has a mapping in graph 2 (I*(E1) subset E2), with angle(e1) = angle(e2)
		[
			Exist(
					(I[E1[e1][0]] == E2[e2][p]) & (I[E1[e1][1]] == E2[e2][(p + 1) % 2])
				for e2 in range(NE_2) for p in range(2) if O1[e1] == O2[e2]
			) for e1 in range(NE_1)
		]
	)

    # ===== SOLVE =====
    cnt = 0
    while solve() is SAT:
        cnt += 1
        print(f"Solution {cnt}: {values(I)}")
        satisfy(I != values(I))  # Exclude the current solution to find new ones
        process_mapping(cnt)
  
    print("No more solutions.")
