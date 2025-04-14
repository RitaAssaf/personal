import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot 

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

#dictionnary to have names as linear order and still manipulate the matrix using indices
tel={}
count=0
# Add nodes with their positions
for i in range(num_rows):
	for j in range(num_cols):
		if X[i][j] == 1:
			tel[f'{i},{j}'] = count
			
			G.add_node(count, position=(j, i))
			count+=1
			#G.add_node((i, j), position=(j, i))

# Add edges based on requirements
for i in range(num_rows):
	for j in range(num_cols):
		if X[i][j] == 1:
			# Check horizontally to the right
			for k in range(j + 1, num_cols):
				if X[i][k] == 1:
					node_a=tel[f'{i},{j}']
					node_b=tel[f'{i},{k}']
					G.add_edge(node_a, node_b)
					break
			# Check vertically downward
			for k in range(i + 1, num_rows):
				if X[k][j] == 1:
					node_a=tel[f'{i},{j}']
					node_b=tel[f'{k},{j}']
					G.add_edge(node_a, node_b)
					break

# Export graph to Graphviz DOT format
dot_filename = "dat/samplegraph.dot"
write_dot(G, dot_filename)
print(f"Graph saved to {dot_filename}")

# Let's draw the graph!
pos = nx.get_node_attributes(G, "position")
plt.figure(figsize=(8, 10))  # Set figure size
nx.draw(G, pos, with_labels=True, node_size=100, font_size=8)  # Draw graph with labels
plt.show() 
