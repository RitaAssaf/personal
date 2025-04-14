import networkx as nx
import numpy as np
from networkx.drawing.nx_pydot import write_dot
import pydot

num_rows = 20
num_cols = 10
num_nodes = 100
seed = 0

# Build matrix X
rng = np.random.default_rng(seed=seed)
X = rng.random(size=(num_rows, num_cols))

def search_threshold(X, N):
	"""Find a threshold that ensures exactly N elements in X are above it."""
	flattened = np.sort(X.ravel())[::-1]
	if N > len(flattened):
		raise ValueError("N exceeds the total number of elements in the matrix.")
	return flattened[N - 1]

threshold = search_threshold(X, num_nodes)
X[X>=threshold] = 1
X[X<threshold] = 0

print(f"Matrix X contains {np.count_nonzero(X)} elements.")


# Create graph G from X
G = nx.Graph()

# Add nodes with their positions
for i in range(num_rows):
	for j in range(num_cols):
		if X[i][j] == 1:
			G.add_node((i, j), position=(j, i))

# Add edges based on requirements
for i in range(num_rows):
	for j in range(num_cols):
		if X[i][j] == 1:
			# Check horizontally to the right
			for k in range(j + 1, num_cols):
				if X[i][k] == 1:
					G.add_edge((i, j), (i, k))
					break
			# Check vertically downward
			for k in range(i + 1, num_rows):
				if X[k][j] == 1:
					G.add_edge((i, j), (k, j))
					break

# Should we remove nodes without edges? maybe, maybe not

# Let's draw the graph!
pos = nx.get_node_attributes(G, "position")
nx.draw(G, pos)
# Export graph to DOT file
write_dot(G, "graph.dot")

# Use pydot to generate PNG
graph = pydot.graph_from_dot_file("graph.dot")[0]
graph.write_png("graph.png")

print("Graph exported as graph.png")
