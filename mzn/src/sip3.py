from pycsp3 import *
import os
import sys
import argparse
from pathlib import Path

import networkx as nx
import pydot
from minizinc import Model, Solver, Instance

def load(instance, graph_file, id):
	
	# Load graph
	graph = nx.drawing.nx_agraph.read_dot(graph_file)

	# Plot input graph
	pydot.graph_from_dot_file(graph_file)[0].write_png(f'res/{Path(os.path.basename(graph_file)).stem}.png')

	# Get graph edges and labels
	edges = graph.edges
	labels = nx.get_node_attributes(graph, 'label')
	angles = nx.get_edge_attributes(graph, 'order')

	# Set instance data
	instance[f'NV_{id}'] = graph.number_of_nodes()
	instance[f'NE_{id}'] = graph.number_of_edges()
	instance[f'V{id}'] = [label for label in labels.values()]
	instance[f'E{id}'] = list()
	instance[f'A{id}'] = list()
	for n1, n2 in edges:
		instance[f'E{id}'].append((int(n1), int(n2)))
		instance[f'A{id}'].append('l' if angles[n1, n2] == 'l' else 'c')






# Function to define subgraph isomorphism model
def subgraph_isomorphism(pattern_graph, target_graph):
    n_pattern = len(pattern_graph)  # number of nodes in the pattern graph
    n_target = len(target_graph)  # number of nodes in the target graph

    # Decision variables: mapping[i] = j means node i in pattern is mapped to node j in target
    mapping = VarArray(size=n_pattern, dom=range(n_target))

    # Ensure all nodes in the pattern graph are mapped to different nodes in the target graph
    satisfy(
        AllDifferent(mapping)
    )

    # Ensure adjacency relations are preserved: if i and j are adjacent in pattern,
    # then mapping[i] and mapping[j] must be adjacent in the target
    satisfy(
        (mapping[i], mapping[j]) in {(u, v) for u in range(n_target) for v in target_graph[u]}
        for i in range(n_pattern) for j in pattern_graph[i] if i < j
    )

    # Solve the problem and print the solution
    if solve() is SAT:
        print("subgraph found")
        print("Pattern to Target mapping:", {i: mapping[i].value for i in range(n_pattern)})
    else:
        print("not found")

# Example usage
if __name__ == "__main__":
    pattern_graph = [[1], [0, 2], [1]]  # Example pattern graph: 0-1-2
    target_graph = [[1, 2], [0, 3], [0, 3], [1, 2]]  # Example target graph

    subgraph_isomorphism(pattern_graph, target_graph)
