import os
import sys
import networkx as nx
from pycsp3 import *

def load_graph(graph_file):
    """ Load a graph from a .dot file and return nodes, edges, and angles. """
    graph = nx.drawing.nx_agraph.read_dot(graph_file)
    edges = list(graph.edges)
    labels = nx.get_node_attributes(graph, 'label')
    angles = nx.get_edge_attributes(graph, 'order')

    # Convert node labels to indices
    node_map = {n: i + 1 for i, n in enumerate(graph.nodes)}
    edge_list = [(node_map[n1], node_map[n2]) for n1, n2 in edges]
    angle_list = ['l' if angles.get((n1, n2), 'c') == 'l' else 'c' for n1, n2 in edges]

    return len(graph.nodes), len(edges), list(labels.values()), edge_list, angle_list

# Parse arguments for pattern and target files
pattern_file = sys.argv[1] if len(sys.argv) > 1 else "dat/pan.dot"
target_file = sys.argv[2] if len(sys.argv) > 2 else "dat/net.dot"

# Load pattern and target graphs
NV_1, NE_1, V1, E1, A1 = load_graph(pattern_file)
NV_2, NE_2, V2, E2, A2 = load_graph(target_file)

# Decision variable I[v] -> maps node v in the pattern graph to a node in the target graph
I = VarArray(size=NV_1, dom=range(1, NV_2 + 1))

# Constraint 1: All nodes in the pattern graph must map to different nodes in the target graph
satisfy(
    AllDifferent(I)
)

# Constraint 2: Each edge in the pattern graph must have a corresponding edge in the target graph with the same angle
satisfy(
    [
        exists(e2 in range(len(E2)))(
            ((I[n1 - 1], I[n2 - 1]) == E2[e2] or (I[n2 - 1], I[n1 - 1]) == E2[e2])
            & (A1[i] == A2[e2])
        )
        for i, (n1, n2) in enumerate(E1)
    ]
)

# Solve the CSP and collect all solutions manually
solutions = []
while solve() is not None:
    solutions.append(values(I))  # Collect the current solution
    if not nextSolution():  # Move to the next solution if available
        break

# Output solutions
if solutions:
    print(f"Found {len(solutions)} solutions.")
    for i, solution in enumerate(solutions):
        mapping = [solution[v] for v in range(NV_1)]
        print(f"Solution {i + 1}: {[V1[v] + ' -> ' + V2[mapping[v] - 1] for v in range(NV_1)]}")
else:
    print("No solution found.")
