import networkx as nx
from collections import Counter
from circle import Circle
from class_label_order import LabelOrder

def hopcroft(m, m_prime):
	# Create a bipartite graph
	B = nx.Graph()
	
	# Add nodes for each element in m and m'
	left_nodes = ['m_' + str(i) for i in range(len(m))]
	right_nodes = ['m_prime_' + str(j) for j in range(len(m_prime))]
	
	B.add_nodes_from(left_nodes, bipartite=0)  # Left set (m)
	B.add_nodes_from(right_nodes, bipartite=1)  # Right set (m_prime)
	
	# Add edges based on the partial order (a_i <= b_j)
	for i, a_i in enumerate(m):
		for j, b_j in enumerate(m_prime):
			if a_i <= b_j:
				B.add_edge('m_' + str(i), 'm_prime_' + str(j))
	
	# Run Hopcroft-Karp algorithm to find maximum matching, specifying top_nodes
	matching = nx.bipartite.maximum_matching(B, top_nodes=left_nodes)
	
	# Check if matching covers all elements of m (left set)
	matched_left = [node for node in matching if node in left_nodes]
	
	# If all elements of m are matched, return True (m <= m')
	return len(matched_left) == len(m)


def build_partial_order(node_structure):
	partial_order = {}
	
	nodes = list(node_structure.keys())
	
	for i, node_a in enumerate(nodes):
		partial_order[node_a] = []
		degree_a, neighbor_degrees_a = node_structure[node_a]
		
		for j, node_b in enumerate(nodes):
			if i == j:
				continue
			
			degree_b, neighbor_degrees_b = node_structure[node_b]
			
			# Check the degree condition and neighbor degree condition
			if degree_a <= degree_b and hopcroft(neighbor_degrees_a, neighbor_degrees_b):
				partial_order[node_a].append(node_b)
	
	return partial_order

def build_partial_order_2(node_structure):
	partial_order = {}
	order_labels = {}
	nodes = list(node_structure.keys())
	
	j=1
	for i, node_a in enumerate(nodes):
	
		degree_a, neighbor_degrees_a = node_structure[node_a]
		
		labels= list( order_labels.keys())

		exist= False
		if len( order_labels)==0:
		
			order_labels['m_' + str(j)] = (degree_a, neighbor_degrees_a,[node_a])
			j=j+1
		else:
			for k, label_k in enumerate(labels):
				degree_k, neighbor_degree_k, noeuds_k=  order_labels[label_k]
				if degree_k== degree_a and Counter(neighbor_degrees_a) == Counter(neighbor_degree_k): #Counter(list1) This checks whether both lists have the same elements with the same frequency, regardless of the order.            
					exist= True             
					break
			
			if exist == False:
				order_labels['m_' + str(j)] = (degree_a, neighbor_degrees_a, [node_a])
				j=j+1
	   
	return  order_labels



def build_partial_order_3(node_structure):
	partial_order = {}
	order_labels = []
	nodes = list(node_structure.keys())
	
	j=1
	for i, node_a in enumerate(nodes):
	
		degree_a, neighbor_degrees_a = node_structure[node_a]
		
		
		exist= False
		if len( order_labels)==0:
			order_labels.append(LabelOrder('m_' + str(j), degree_a, neighbor_degrees_a, [node_a],[] ))
			#order_labels['m_' + str(j)] = (degree_a, neighbor_degrees_a,[node_a])
			j=j+1
		else:
			for label_k in order_labels:
				if label_k._label== degree_a and Counter(neighbor_degrees_a) == Counter(label_k._neighbors_labels): #Counter(list1) This checks whether both lists have the same elements with the same frequency, regardless of the order.            
					exist= True   
					label_k.add_node(node_a)         
					break
			
			if exist == False:
				order_labels.append(LabelOrder('m_' + str(j), degree_a, neighbor_degrees_a, [node_a],[]))
				j=j+1
				for label_i in order_labels:
					if label_i._label <= order_labels[-1]._label and hopcroft(label_i._neighbors_labels , order_labels[-1]._neighbors_labels):
						label_i._preceds.append(order_labels[-1]._name )
	   
	return  order_labels



def ILF(Gp, Gt,D):
	# Degree labeling for both graphs
	labeling = {node: Gp.degree(node) for node in Gp.nodes}
	
	for node in Gt.nodes:
		labeling[node] = Gt.degree[node]
	
	for n in Gp.nodes:
		for t in Gt.nodes:
			if not labeling[n] <= labeling[t]:
			 D[n].remove(t)
	# Neighborhood extension (just printing nodes as an example)
	# for n in set(Gp.nodes).union(set(Gt.nodes)):
	#     print(n)

	# Build the structure: degree.{degrees of neighbors}
	# dict[Any, tuple[int, list[int]]]
	node_structure = {}


	for node in Gp.nodes:
		node_degree = Gp.degree(node)
		neighbor_degrees = [Gp.degree(neighbor) for neighbor in Gp.neighbors(node)]
		node_structure[node] = (node_degree, neighbor_degrees)  # Store the degree and neighbor's degrees

	for node in Gt.nodes:
		node_degree = Gt.degree(node)  
		neighbor_degrees = [Gt.degree(neighbor) for neighbor in Gt.neighbors(node)]
		node_structure[node] = (node_degree, neighbor_degrees)  # Store the degree and neighbor's degrees

 
	for node, (degree, neighbor_degrees) in node_structure.items():
		print(f"{node}: {degree}.{{{', '.join(map(str, neighbor_degrees))}}}")
	
	

	for label_k in build_partial_order_3(node_structure):
		print(label_k)
##############################################################################
# Example graphs
Gp = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])  # Simple cycle

Gt = nx.Graph([  # Example target graph Gt with different node labels
	('a', 'c'), ('c', 'b'), ('c', 'd'), ('d', 'e'), ('e', 'f'),
	('f', 'g'), ('f', 'h'), ('h', 'i'), ('i', 'j'), ('j', 'k'), ('k', 'h')
])

# Example CSP variables
Lvar = {1: 'x1', 2: 'x2', 3: 'x3', 4: 'x4'}  # Variable mapping

# Initial domain of variables, using the correct node labels for Gt
D = {
	1: {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'},
	2: {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'},
	3: {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'},
	4: {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'}
}


################################################################
# Call the ILF function with Gp and Gt
ILF(Gp, Gt, D)