import networkx as nx
import matplotlib.pyplot as plt
import inflect
from collections import Counter
from circle import Circle
from class_label_order import LabelOrder
from class_node import Node

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


#	print(f"does m_1 preceds m_4?: {oneprecedstwo('m_1', 'm_4', ordered_labels)}")

def oneprecedstwo(m, m_prime, ordered_labels):
    # Find label and label_prime in a single loop
    label, label_prime = None, None
    for x in ordered_labels:
        if x._name == m:
            label = x
        if x._name == m_prime:
            label_prime = x
        # Stop early if both are found
        if label and label_prime:
            break
    
    # Check if either label or label_prime is None
    if label is None or label_prime is None:
        print(f"label '{m}' or '{m_prime}' not found in ordered_labels")
        return False

    # Ensure `_preceds` is iterable and check for label_prime in it
    if not isinstance(label._preceds, list):
        print(f"Warning: _preceds attribute for '{label._name}' is not a list.")
        return False

    # Check if label_prime's name is in label's preceds list
    result = label_prime._name in label._preceds
   # print(f"Checking if '{label_prime._name}' is in '{label._name}'._preceds: {result}")
   # print(f"prime: {label_prime} and label: {label}")
    return result


def hopcroft_multiset(m, m_prime, ordered_labels):
	#print(f"does 'm_5', 'm_5' preceds m_3', 'm_4?: {hopcroft_multiset(['m_5', 'm_5'],['m_4'], ordered_labels)}")

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
			if oneprecedstwo( a_i, b_j, ordered_labels):
				B.add_edge('m_' + str(i), 'm_prime_' + str(j))
	
	# Run Hopcroft-Karp algorithm to find maximum matching, specifying top_nodes
	matching = nx.bipartite.maximum_matching(B, top_nodes=left_nodes)
	
	# Check if matching covers all elements of m (left set)
	matched_left = [node for node in matching if node in left_nodes]
	
	# If all elements of m are matched, return True (m <= m')
	return len(matched_left) == len(m)



def build_partial_order_3(nodes):
	partial_order = {}
	order_labels = []
	
	j=1
	for node_a in nodes:
	
		exist= False
		if len( order_labels)==0:
			order_labels.append(LabelOrder('m_' + str(j), node_a._label, node_a._neighbors_labels, [node_a._name],[] ))
			j=j+1
			#comparer l'élt qu'on vient d'ajouter avec les labels de la liste 
			# dans ce cas len=0 l'elt label m1 sera ajouté à preceds de lui même
			for label_i in order_labels:
				# comparaison qui dépend de degré comment comparer m1 m2
					if label_i._label <= order_labels[-1]._label and hopcroft(label_i._neighbors_labels , order_labels[-1]._neighbors_labels):
						label_i._preceds.append(order_labels[-1]._name )
	   		# à remplacer par ajout direct de preceds puisqu'il y aura qu'un seul element et c'est l'élément lui même ajouté 
			# très important à ajouter sinon l'element n'est pas comparé à lui même et donc 1,2,3,4,j n'st pas comparé par exemple j appartient au domaine de 1234
		else:
			for label_k in order_labels:
				if label_k._label== node_a._label and Counter(node_a._neighbors_labels) == Counter(label_k._neighbors_labels): #Counter(list1) This checks whether both lists have the same elements with the same frequency, regardless of the order.            
					exist= True  
					# un noeud a un label qui existe déjà 
					label_k.add_node(node_a._name)         
					break
			
			if exist == False:
				order_labels.append(LabelOrder('m_' + str(j), node_a._label, node_a._neighbors_labels, [node_a._name],[] ))
				j=j+1
				for label_i in order_labels:
					if label_i._label <= order_labels[-1]._label and hopcroft(label_i._neighbors_labels , order_labels[-1]._neighbors_labels):
						label_i._preceds.append(order_labels[-1]._name )
	   
	return  order_labels

#LabelOrder(self, name, label, neighbors_labels, nodes, preceds):
#Node(self,name, label, neighbors_labels, domain, ispattern)

def build_partial_order_4(nodes, ordered_labels):
	partial_order = {}
	new_order_labels = []
	
	j=1
	label_letter= ordered_labels[0]._name.split('_')[0]
	label_letter=chr(ord(label_letter) + 1)
	#print(f"label_letter= {label_letter}")
	for node_a in nodes:
	
		label_label_ajouté= node_a._label
		neighbors_label_ajouté=node_a._neighbors_labels
		exist= False
		if len( new_order_labels)==0:
			new_order_labels.append(LabelOrder(label_letter +'_'+ str(j), node_a._label, node_a._neighbors_labels, [node_a._name],[] ))
			j=j+1
			
   			#Suppose we have n1= m1.{m1,m1} and want to add n2=m2.{m3}, n1<n2
  			# check m1< m2 i.e. m2 in m1.preceds and hopcroft multiset ({m1, m1}, {m3})
			for label_i in new_order_labels: 
       
				objet_label_label_boucle=[x for x in ordered_labels if x._name == label_i._label][0] # get m1 from the old ordered labels
			
				if  label_label_ajouté in objet_label_label_boucle._preceds and hopcroft_multiset(label_i._neighbors_labels, neighbors_label_ajouté, ordered_labels):
					label_i._preceds.append(new_order_labels[-1]._name )
	   		# à remplacer par ajout direct de preceds puisqu'il y aura qu'un seul element et c'est l'élément lui même ajouté 
			# très important à ajouter sinon l'element n'est pas comparé à lui même et donc 1,2,3,4,j n'st pas comparé par exemple j appartient au domaine de 1234
		else:
			for label_k in new_order_labels:
				if label_k._label== node_a._label and Counter(node_a._neighbors_labels) == Counter(label_k._neighbors_labels): #Counter(list1) This checks whether both lists have the same elements with the same frequency, regardless of the order.            
					exist= True  
					# un noeud a un label qui existe déjà 
					label_k.add_node(node_a._name)         
					break
			
			if exist == False:
				new_order_labels.append(LabelOrder(label_letter +'_'+ str(j), node_a._label, node_a._neighbors_labels, [node_a._name],[] ))
				j=j+1
				for label_i in new_order_labels:
       			#on retrouve le label de la liste m déjà construite
					objet_label_label_boucle=[x for x in ordered_labels if x._name == label_i._label][0] 
			
					if  label_label_ajouté in objet_label_label_boucle._preceds and hopcroft_multiset(label_i._neighbors_labels, neighbors_label_ajouté, ordered_labels):
						label_i._preceds.append(new_order_labels[-1]._name )
	return  new_order_labels


def ILF(Gp, Gt, posp, post):
	p = inflect.engine()
	#INITIAL DOMAINS##############################################
	print('	#INITIAL DOMAINS##############################################')
	
	#  def __init__(self,name, label, neighbors_labels, domain, pattern):
	nodes_array = [
    Node(node,"" , [], list(Gt.nodes()), 1) 
    for node in Gp.nodes()
    ]
	
	#list(Gp.degree(neighbor) for neighbor in Gp.neighbors(node))
	nodes_array.extend([
    Node(node,"", [],[], 0) 
    for node in Gt.nodes()
	])

	for node in nodes_array:
		print(node)

	#FIRST FILTERING ##############################################
	print('	#FIRST FILTERING##############################################')

	
	for node in nodes_array:
		if node._ispattern:
			node._label=Gp.degree(node._name)
		else:
			node._label=Gt.degree(node._name)

	#DOMAIN FILTERING############
	for node in nodes_array:
		for node_j in node._domain:
			if not node._label <= [x for x in nodes_array if x._name == node_j][0]._label:
				node._domain.remove(node_j)
	
	
	for node in nodes_array:
		print(node)

	#FIRST ITERATION##############################################
	
	print('	#1st ITERATION##############################################')
	
	for node in nodes_array:
		if node._ispattern:
			node._label=Gp.degree(node._name)
			node._neighbors_labels=list(Gp.degree(neighbor) for neighbor in Gp.neighbors(node._name))
		else:
			node._label=Gt.degree(node._name)
			node._neighbors_labels=list(Gt.degree(neighbor) for neighbor in Gt.neighbors(node._name))


	ordered_labels= build_partial_order_3(nodes_array )
	
	#DOMAIN FILTERING###################################
	for label in ordered_labels:
		nodes_preced=[]
		#prendre les noeuds preceds dans le domaine du label _ispattern
		for label_preced in label._preceds: #m1 < m2,m3,m4
			labelpreced= [x for x in ordered_labels if x._name == label_preced ][0] # prendre m2
			
			#prendre les noeuds qui ont label m2
			for nodepreced in labelpreced._nodes:
				#vérifier que le noeud n'est pas pattern avant de l'ajouter
				if not [x for x in nodes_array if x._name == nodepreced][0]._ispattern:
					nodes_preced.append(nodepreced)
			#pour les noeus qui ont ce label ajouter les noeuds preceds au domaine
		for node in label._nodes:
			noeud= [x for x in nodes_array if x._name == node][0]
			noeud._domain= nodes_preced
	

	print('## NODES ARRAY ##############################')
	for node in nodes_array:
		print(node)

	print('## LABELS ARRAY ##############################')
	for label in ordered_labels:
		print(label)

	

    # ITERATIONS LOOP ##############################################
	for i in range(2, 7):
		domains_unchanged= True
		num_labels_unchanged= True

		print(f"	#{p.ordinal(i)} ITERATION  ############################################")
		
		for node in nodes_array:
			node._label=[x for x in ordered_labels if node._name in x._nodes ][0]._name
			
		# Create a lookup dictionary for name-to-node mappings
		node_dict = {node._name: node for node in nodes_array}

		# Update each node's neighbor labels using the dictionary
		for node in nodes_array :
			if node._ispattern:
				node._neighbors_labels=list([node_dict[neighbor]._label for neighbor in Gp.neighbors(node._name) if neighbor in node_dict])
			else:
				node._neighbors_labels=list([node_dict[neighbor]._label for neighbor in Gt.neighbors(node._name) if neighbor in node_dict])
		
		
		
		new_ordered_labels= build_partial_order_4(nodes_array , ordered_labels)
		
		#DOMAIN FILTERING###################################
		#pour chaque label de l'ordre, prendre les labels qui suivent 
		#m1< m2, m3, m4 : prendre  m2, m3, m4  
		#et pour tous les noeuds qui ont lable m1, ajouter les noeuds qui ont label m2 ou m3 ou m4 au domaine de m1
		for label in new_ordered_labels:
			nodes_preced=[]
			#ajouter les noeuds aux domaines
			for label_preced in label._preceds: #m1 < m2,m3,m4

				# prendre m2 en tant qu'objet			
				labelpreced = [x for x in new_ordered_labels if x._name == label_preced] [0]
				
				#prendre les noeuds qui ont label m2
				for nodepreced in labelpreced._nodes:
					#vérifier que le noeud est pattern avant de l'ajouter
					if not [x for x in nodes_array if x._name == nodepreced][0]._ispattern:
						nodes_preced.append(nodepreced)
			
   			#pour les noeus patterne qui ont ce label affecter les noeuds preceds au domaine
			for node in label._nodes:
				noeud= [x for x in nodes_array if x._name == node][0]
				if noeud._ispattern:
					# si le domaine d'un noeud est différent des noeuds affectés
					if domains_unchanged and Counter(noeud._domain) != Counter(nodes_preced):
						domains_unchanged=False
					noeud._domain= nodes_preced
		
		
		if len(ordered_labels)!= len(new_ordered_labels):
			num_labels_unchanged=False

		# la prochaine itération on utilise les nouveaux labels n1,n2,.. pour comparer o1=n1.{n} et o2=n2.{n3}
		ordered_labels= new_ordered_labels


		print('## NODES ARRAY ##############################')
		for node in nodes_array:
			print(node)

		print('## LABELS ARRAY ##############################')
		for label in new_ordered_labels:
			print(label) 

		if num_labels_unchanged and domains_unchanged:
			print(f"Fixpoint reached at {p.ordinal(i)} iteration############################################# ")
			break
	
	# Draw the graph
	plt.figure(figsize=(8, 6))  # Set the figure size

	if len(Gt.nodes)==len(post):
		nx.draw(Gt, post, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)

	else:
		nx.draw(Gt, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)

	if len(Gp.nodes)==len(posp):
		nx.draw(Gp, posp, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)

	else:
		nx.draw(Gp, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=15)


	# Display the graph
	plt.title("Graph Gt")
	plt.show()


# MAIN #############################################################################

# Instance 1
""" Gp = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])  

Gt = nx.Graph([  # Example target graph Gt with different node labels
	('a', 'c'), ('c', 'b'), ('c', 'd'), ('d', 'e'), ('e', 'f'),
	('f', 'g'), ('f', 'h'), ('h', 'i'), ('i', 'j'), ('j', 'k'), ('k', 'h')
]) """

#Instance 2: exemple P. Frédéric
""" Gp = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1), (4, 5)])  

Gt = nx.Graph([ 
	('a', 'b'), ('a', 'd'), ('b', 'c'), ('b', 'e'), ('c', 'f'), ('d', 'e'),
	('d', 'g'), ('e', 'f'), ('e', 'h'), ('f', 'i'), ('g', 'h'), ('h', 'i')
]) """

#Instance 3: intersections graph de I1
Gp = nx.Graph([('l1', 'c2'), ('l1', 'c1'), ('l2', 'c2'), ('l2', 'c1')])  

Gt = nx.Graph([ 
	('l1p', 'c2p'), ('l2p', 'c1p'), ('l2p', 'c2p'), ('l2p', 'c3p'), ('l2p', 'c5p')
	, ('l3p', 'c5p'),  ('l3p', 'c6p'), ('l4p', 'c4p'),  ('l4p', 'c5p'),  ('l5p', 'c4p') , ('l5p', 'c5p') 
])

post = {
    'l1p': (0, 6), 'l2p': (0, 5), 'l3p': (0, 4), 'l4p': (0, 3),
    'l5p': (0, 2), 'c1p': (2, 6), 'c2p': (2,5), 'c3p': (2,4),
    'c4p': (2, 3), 'c5p': (2, 2), 'c6p': (2,1)
}

posp={'l1': (-1, 2), 'l2': (-1, 1), 'c1': (-1.5,2), 'c2': (-1.5,1)}
################################################################
# Call the ILF function with Gp and Gt

ILF(Gp, Gt, posp, post)