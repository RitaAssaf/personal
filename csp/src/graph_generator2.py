import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

num_rows = 20
num_cols = 10
num_nodes = 100
seed = 0

# Build matrix X
#rng = np.random.default_rng(seed=seed)
rng = np.random.default_rng()  # No fixed seed
X = rng.random(size=(num_rows, num_cols))

def search_threshold(X, N):
	"""Find a threshold that ensures exactly N elements in X are above it."""
	flattened = np.sort(X.ravel())[::-1]
	if N > len(flattened):
		raise ValueError("N exceeds the total number of elements in the matrix.")
	return flattened[N - 1]

threshold = search_threshold(X, num_nodes)
X[X >= threshold] = 1
X[X < threshold] = 0

print(f"Matrix X contains {np.count_nonzero(X)} elements.")

# Create directed graph G
G = nx.DiGraph()
tel = {}  # Dictionary to map matrix indices to node IDs
count = 0

# Add nodes with their positions
for i in range(num_rows):
	for j in range(num_cols):
		if X[i][j] == 1:
			tel[f'{i},{j}'] = count
			G.add_node(count, position=(j, i))  # x=j, y=i
			count += 1

# Add directed edges based on adjacency rules
edges = []
for i in range(num_rows):
	for j in range(num_cols):
		if X[i][j] == 1:
			node_a = tel[f'{i},{j}']
			
			# Check horizontally (right)
			for k in range(j + 1, num_cols):
				if X[i][k] == 1:
					node_b = tel[f'{i},{k}']
					G.add_edge(node_a, node_b)  # a → b (left to right)
					edges.append((node_a, node_b, 90))  # Same row → angle=90
					break
			
			# Check vertically (downward)
			for k in range(i + 1, num_rows):
				if X[k][j] == 1:
					node_b = tel[f'{k},{j}']
					G.add_edge(node_a, node_b)  # a → b (top to bottom)
					edges.append((node_a, node_b, 0))  # Different row → angle=0
					break

timestamp = datetime.now().strftime("%d%m%Y%H%M")

# Generate Graphviz DOT format
dot_filename = f"dat/graph_{timestamp}.dot"

with open(dot_filename, "w") as f:
	f.write("digraph G {\n")
	f.write("    graph [splines=true, nodesep=0.5, rankdir=TB];\n")
	f.write("    node [shape=circle, fixedsize=true, width=0.4, fontsize=10];\n")

	# Add nodes with labels
	for node, pos in nx.get_node_attributes(G, "position").items():
		f.write(f'    {node} [label="{node}"];\n')

	# Add rank=same constraints
	row_dict = {}
	for node, pos in nx.get_node_attributes(G, "position").items():
		y_coord = pos[1]
		if y_coord not in row_dict:
			row_dict[y_coord] = []
		row_dict[y_coord].append(str(node))

	for nodes in row_dict.values():
		if len(nodes) > 1:
			f.write(f'    {{ rank=same; {" ".join(nodes)} }};\n')

	# Add edges with angle attributes (only once)
	for node_a, node_b, angle in edges:
		f.write(f'    {node_a} -> {node_b} [angle={angle}];\n')

	f.write("}\n")

print(f"Graph saved to {dot_filename}")

# Draw the graph for reference
pos = nx.get_node_attributes(G, "position")
plt.figure(figsize=(8, 10))
nx.draw(G, pos, with_labels=True, node_size=100, font_size=8, arrows=True)
plt.show()
