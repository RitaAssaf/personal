import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from itertools import combinations
import random
from networkx.drawing.nx_pydot import write_dot
from datetime import datetime


class lcnode:
	def __init__(self, name=None, preceds=None, sublists=None):
		self.name = name
		self.preceds = preceds
		self.sublists =sublists





def generer_sous_listes_ordonnées(liste):
	sous_listes = []
	for i in range(len(liste)):
		for j in range(i, len(liste)):
			sous_listes.append(liste[i:j + 1])  
	return sous_listes

def extraction_arcs(mat:list[list],lab:str):
	# lit une liste de liste pour extraire des arcs sur chaque ligne dont le label est lab
	arc_ext=[]
	for li in mat:
		i = 0
		while i < len(li) - 1:
			if li[i] > -1: #token exist
				j = i + 1
				while j < len(li) and li[j] == -1:
					j = j + 1
				if j < len(li):
					#arc_ext.append((li[i], li[j], {'label': lab}))
					arc_ext.append((li[i], li[j], {'label': lab, 'angle': 0 if lab == 'h' else 90}))
				i = j
			else:
				i = i + 1
	return arc_ext

def cloture_reflexive(G,lab:str):
	for noeud in G.nodes():
		G.add_edge(noeud, noeud)
		G[noeud][noeud]['label']=lab
	return G

def cloture_transitive(G,lab:str):
	G_cloture = nx.transitive_closure(G)
	# Copier les attributs des arêtes du graphe d'origine vers le graphe de la clôture
	for u,v in G_cloture.edges():
		if 'label' not in G_cloture[u][v]:
			G_cloture[u][v]['label'] = lab
	return G_cloture

def aplatir_liste(liste_imbriquee):
	resultat = []
	for i in liste_imbriquee:
		for e in i:
			resultat.append(e)
	return resultat





def get_coordinates(v, n):
	j = (v - 1) // n
	i = (v - 1) % n
	return (i, j)


def nommer(l, label):
	s = "".join(map(str, l)) #concatener la liste des tokens dans la ligne/colonne
	return label + s #ajoute label l ou c

def numerote(mat:list[list]):
	compteur = 0  # Initialisation du compteur
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			if mat[i][j] > -1:
				mat[i][j] = compteur
				compteur += 1
	return mat


def generer_positions_alea(n, p):

	mat = [[-1] * n for _ in range(n)]
	places = random.sample(range(n * n), p)
	# Placer les 1
	for pl in places:
		i, j = divmod(pl, n)  # pl = 7 → divmod(7, 3) → (2, 1)  # Row 2, Column 1 in matrix 3 x 3
		mat[i][j] = 1
	return mat
# Function to extract ordered nodes based on preceds
def sorted_nodes(graph):
	ordered = []
	for node in graph.nodes:
		if node not in ordered:
			ordered.append(node)
		for succ in graph.nodes[node]['preceds']:
			if succ not in ordered:
				ordered.append(succ)
	return ordered


def main():
	# instance
	# positions = [[1, 1, 1, 1],
	#             [1, 0, 1, 0],
	#             [1, 0, 1, 0],
	#            [0, 1, 0, 0]]

	#positions = generer_positions_alea(3, 7)
	#positions = generer_positions_alea(10, 70)
	# positions = generer_positions_alea(10, 40)
	# positions = numerote(positions)
	#positions = [[0, 1, 2], [3, 4, -1], [5, 6, 7]]
	#positions = [[0, 1, 2,3], [-1, 4, 5, 6], [-1, 7, 8,9]]
	positions = [[0, 1, 2], [-1,3, 4], [-1, 5, -1]]
	#print(positions)

	#traitement de l'instance et mise en forme des paramètres (taille, arcs...)
	#nb_nodes = sum(1 for li in positions for val in li if val != 0)
	nb_nodes = sum(1 for li in positions for val in li if val != -1)
	taille_graphique = len(positions)
	positionsT = list(map(list, zip(*positions))) #transpose zip ([[1 2 3], [4 5 6]]) = [1 4] [2 5] [3 6]
	arcs = extraction_arcs(positions,'h')+extraction_arcs(positionsT,'v')

	arcs_h = [arc for arc in arcs if arc[2]['label'] == 'h']
	arcs_v = [arc for arc in arcs if arc[2]['label'] == 'v']

	sup_ligcol=False#pour ne pas afficher les lignes colonnes de taille 1 dans le GLC
	
	# création du graphe de position réduit
	G = nx.DiGraph()
	# for n in ran-ge(nb_nodes):
	# 	G.add_node(n , type='t'),
	for i in range(len(positions)):
		for j in range(len(positions[i])):
			if positions[i][j] > -1:
				G.add_node(positions[i][j], position=(j, i))
	G.add_edges_from(arcs)

	# graphe avec arcs horizontaux
	GH = nx.DiGraph()
	GH.add_nodes_from(range(0, nb_nodes))
	GH.add_edges_from(arcs_h)
	# graphe avec arcs verticaux
	GV = nx.DiGraph()
	GV.add_nodes_from(range(0, nb_nodes))
	GV.add_edges_from(arcs_v)

	#Graphe de position (avec transitivité)
	GHT = cloture_transitive(GH,'h')
	GVT = cloture_transitive(GV,'v')
	GT = nx.compose(GHT, GVT)

	# Extraction des lignes et colonnes
	lignes = list(nx.find_cliques(GHT.to_undirected()))
	colonnes = list(nx.find_cliques(GVT.to_undirected()))
	edges = []


#########################################################################"######"
	# création du graphe lignes/colonnes maximales
	GLC_max = nx.Graph()


	# add an attribute preceds to each node: for each iteration in the loop when
	# a node is added preceds of the nodes of the list is updated and takes 
	# the added node. Example for lignes= [[0,1,2],[3,4],[5]], 
	# first node added is l012, next l34 is added and l012.preceds becomes [l34], 



	# List to keep track of previously added nodes
	added_nodes = []
	for li in lignes:
		li=sorted(li)
		node_name = nommer(li, 'l')
		GLC_max.add_node(node_name, type='l', preceds=[])	
		# Update preceds attribute of previous nodes
		for prev_node in added_nodes:
			GLC_max.nodes[prev_node]['preceds'].append(node_name)
		
		# Add current node to the list of added nodes
		added_nodes.append(node_name)




		# List to keep track of previously added nodes
	added_nodes_columns = []
	for co in colonnes:
		co=sorted(co)
		node_name = nommer(co, 'c')
		GLC_max.add_node(node_name, type='c', preceds=[])	
		# Update preceds attribute of previous nodes
		for prev_node in added_nodes_columns:
			GLC_max.nodes[prev_node]['preceds'].append(node_name)
		
		# Add current node to the list of added nodes
		added_nodes_columns.append(node_name)

		# Print the graph nodes with attributes
	# for node, data in GLC_max.nodes(data=True):
	# 	print(node, data)


	for li in lignes:
		for co in colonnes:
			if set(li) & set(co): # computes the intersection between these two sets
				GLC_max.add_edge(nommer(sorted(li), 'l'), nommer(sorted(co), 'c'))
				edges.append((nommer(sorted(li), 'l'), nommer(sorted(co), 'c')))


############################################################################
	sublists = {}
	all_lignes = []
	lines_names = []
	for li in lignes:
		li=sorted(li)
		line_name= nommer(li, 'l')
		sublists[line_name]=generer_sous_listes_ordonnées(li)
		all_lignes.append(sublists[line_name])
	all_colonnes = []
	for co in colonnes:
		co=sorted(co)
		col_name= nommer(co, 'c')
		sublists[col_name]=generer_sous_listes_ordonnées(co)
		all_colonnes.append(sublists[col_name])
	all_colonnes = aplatir_liste(all_colonnes)
	all_lignes = aplatir_liste(all_lignes)
	# Supression des lignes et colonnes de taille 1 pour la visibilité
	if sup_ligcol:
		all_lignes=[li for li in all_lignes if len(li) > 1]
		all_colonnes = [col for col in all_colonnes if len(col) > 1]

	# création du graphe avec toutes lignes/colonnes
	GLC = nx.Graph()
	
	GLC.add_nodes_from([
	(
		nommer(li, 'l'), 
		{
			'type': 'l',
			'sublists': sublists[nommer(li, 'l')] if nommer(li, 'l') in sublists else "",  # Comma added
			'preceds': GLC_max.nodes[nommer(li, 'l')]['preceds'] if nommer(li, 'l') in GLC_max.nodes else "",
			'card' : len(li)
		}
	) 
	for li in all_lignes
	])

	GLC.add_nodes_from([
	(
		nommer(co, 'c'), 
		{
			'type': 'c',
			'sublists': sublists[nommer(co, 'c')] if nommer(co, 'c') in sublists else "",  # Comma added
			'preceds': GLC_max.nodes[nommer(co, 'c')]['preceds'] if nommer(co, 'c') in GLC_max.nodes else "",
			'card' : len(co)
		}
	) 
	for co in all_colonnes
	])

	for lc_complete in GLC_max.nodes:
		for sublist in sublists[lc_complete]:
			if lc_complete.startswith('l'):
				GLC.nodes[nommer(sublist, 'l')]['preceds'] = GLC.nodes[lc_complete]['preceds']
			else:
				GLC.nodes[nommer(sublist, 'c')]['preceds'] = GLC.nodes[lc_complete]['preceds']


	for li in all_lignes:
		for co in all_colonnes:
			if set(li) & set(co):
				GLC.add_edge(nommer(li, 'l'), nommer(co, 'c'))

	# création de l'hypergraphe de Stell avec uniquement les lignes et colonnes complètes
	HST = nx.DiGraph()
	HST.add_nodes_from(GLC_max.nodes(data=True))
	HST.add_nodes_from(G.nodes(data=True))
	for n in G.nodes():
		HST.add_edge(n, n)
	for li in lignes:
		for n in G.nodes():
			if n in li:
				HST.add_edge(nommer(li, 'l'), n)
	for co in colonnes:
		for n in G.nodes():
			if n in co:
				HST.add_edge(nommer(co, 'c'), n)

	# Graphe de positions avec la disposition en grille
	# positions pour le dessin
	if positions == []:
		# si on utilise une représentation sans avoir une grille au départ
		# mais juste la liste des arcs et le graphe G
		pos = {}
		for node in G.nodes():
			x, y = get_coordinates(node, taille_graphique)
			pos.update({node: (x, -y)})
	else:
		pos = {}
		# for x in range(taille_graphique):
		# 	for y in range(taille_graphique):
		# 		if positions[x][y] != 0:
		# 			pos.update({positions[x][y]: (y,-x)})
	
	# Choix des affichages 

	affichage={'GP':True,'GLCRed':False,'GLCall':True,'HS':False}

	# Affichage des deux graphes de positions (réduit et avec transitivité
	if affichage['GP']:
		
		timestamp = datetime.now().strftime("%d%m%Y%H%M%S")

		# Generate Graphviz DOT format
		dot_filename = f"../dat/apositions-{timestamp}.dot"
		#write_dot(G, dot_filename)
		with open(dot_filename, "w") as f:
			f.write("digraph G {\n")
			f.write("    graph [splines=false, nodesep=0.5, rankdir=TB];\n")
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

			#Add edges with angle attributes (only once)
			for node_a, node_b, attributes in arcs:
				#f.write(f'    {node_a} -> {node_b} [{angle}];\n')
				attr_str = ", ".join(f'{key}="{value}"' if isinstance(value, str) else f"{key}={value}" for key, value in attributes.items())
				f.write(f'    {node_a} -> {node_b} [{attr_str}];\n')

			f.write(f"//{positions} \n")

			f.write("}\n")

		print(f"Graph saved to {dot_filename}")




#####################################################################################
#affichage

	# Graphe avec lignes et colonnes
	if affichage['GLCRed']:
		
		timestamp = datetime.now().strftime("%d%m%Y%H%M%S")

		# using l012, l34 token format
		dot_filename = f"../lcres/aGLC_tokens_{timestamp}.dot"
		#write_dot(GLC_max, dot_filename)
		# Append rank constraints for ordered nodes
		ordered_nodes = sorted_nodes(GLC_max)
	
		# Create a mapping of node names to indices
		node_index_map = {node: str(i) for i, node in enumerate(ordered_nodes)}
		# Separate nodes into 'l' and 'c' groups
		l_nodes = [node for node in ordered_nodes if node.startswith('l')]
		c_nodes = [node for node in ordered_nodes if node.startswith('c')]
		# Get indices of line nodes ('l' nodes)
		l_nodes_indices = [node_index_map[node] for node in ordered_nodes if node.startswith('l')]
		# Get indices of line nodes ('c' nodes)
		c_nodes_indices = [node_index_map[node] for node in ordered_nodes if node.startswith('c')]
		with open(dot_filename, "a") as f:
			f.write("strict graph G {\n")
			f.write("    graph [splines=true, nodesep=0.5, rankdir=TB];\n")
			f.write("    node [shape=circle, fixedsize=true, width=0.4, fontsize=10];\n")

			# Add nodes with labels
			for node, t in nx.get_node_attributes(G, "type").items():
				f.write(f'    {node} [label="{node}"];\n')
			for node_a, node_b in edges:
				f.write(f'    {node_a} -- {node_b} ;\n')
			

			f.write("\n    // Ensure horizontal order\n")
			f.write(f"    {{ rank=same; {' '.join(l_nodes)} }}\n")
			f.write(f"    {{ rank=same; {' '.join(c_nodes)} }}\n")
			
			f.write("\n    // Invisible edges to enforce left-to-right order\n")
			for i in range(len(ordered_nodes) - 1):
				if ordered_nodes[i].startswith('l') and ordered_nodes[i+1].startswith('l'):
					f.write(f"    {ordered_nodes[i]} -- {ordered_nodes[i+1]} [style=invis];\n")
				elif ordered_nodes[i].startswith('c') and ordered_nodes[i+1].startswith('c'):
					f.write(f"    {ordered_nodes[i]} -- {ordered_nodes[i+1]} [style=invis];\n")
			f.write("}\n")
			print(f"DOT '{dot_filename}' upd")



		timestamp = datetime.now().strftime("%d%m%Y%H%M%S")

		# Generate Graphviz DOT format
		dot_filename_label = f"../lcres/aGLC_{timestamp}.dot"
		


		with open(dot_filename_label, "w") as f:
			f.write("strict graph G {\n")
			f.write("    graph [splines=true, nodesep=0.5, rankdir=TB];\n")
			f.write("    node [shape=circle, fixedsize=true, width=0.4, fontsize=10];\n")

			# Add nodes with labels replaced by indices
			# for node, index in node_index_map.items():
			# 	f.write(f'    {index} [label="{index}"];\n')
			for node, index in node_index_map.items():
				node_type = GLC_max.nodes[node]['type']
				preceds = ','.join(node_index_map[succ] for succ in GLC_max.nodes[node]['preceds'])
				f.write(f'    {index} [label="{index}", type="{node_type}", preceds="{preceds}"];\n')
			
			# Add edges with indices
			for edge in GLC_max.edges:
				f.write(f'    {node_index_map[edge[0]]} -- {node_index_map[edge[1]]};\n')

			f.write("\n    // Ensure horizontal order\n")
			f.write(f"    {{ rank=same; {' '.join(l_nodes_indices)} }}\n")
			f.write(f"    {{ rank=same; {' '.join(c_nodes_indices)} }}\n")
			f.write("\n    // Invisible edges to enforce left-to-right order\n")
			for i in range(len(ordered_nodes) - 1):
				if ordered_nodes[i].startswith('l') and ordered_nodes[i+1].startswith('l'):
					f.write(f"    {node_index_map[ordered_nodes[i]]} -- {node_index_map[ordered_nodes[i+1]]} [style=invis];\n")
				elif ordered_nodes[i].startswith('c') and ordered_nodes[i+1].startswith('c'):
					f.write(f"    {node_index_map[ordered_nodes[i]]} -- {node_index_map[ordered_nodes[i+1]]} [style=invis];\n")
			
			f.write("}\n")

		print(f"DOT file '{dot_filename_label}' updated with horizontal ordering constraints and edges using indices.")



	# Graphe avec toutes les lignes colonnes
	if affichage['GLCall']: 
		timestamp = datetime.now().strftime("%d%m%Y%H%M%S")

		# l012 tokens format
		dot_filename = f"../lcres/agraph-lc-{timestamp}.dot"

		# Separate nodes into 'l' and 'c' groups
		l_nodes = [node for node in GLC.nodes if node.startswith('l')]
		c_nodes = [node for node in GLC.nodes if node.startswith('c')]

		with open(dot_filename, "a") as f:
			f.write("strict graph G {\n")
			f.write("    graph [splines=true, nodesep=0.5, rankdir=TB];\n")
			f.write("    node [shape=circle, fixedsize=true, width=0.4, fontsize=10];\n")

			# Add nodes with label, type, and preceds attributes
			for node in GLC.nodes:
				node_type = GLC.nodes[node].get('type', "")
				preceds = ",".join(map(str, GLC.nodes[node].get('preceds', [])))  # Join list if exists, else ""
				f.write(f'    {node} [label="{node}", type="{node_type}", preceds="{preceds}"];\n')

			# Add edges
			for node_a, node_b in GLC.edges:
				f.write(f'    {node_a} -- {node_b} ;\n')

			f.write("}\n")
			print(f"DOT saved in :'{dot_filename}'")

#################################################################################
		#indexes format 
		dot_filename = f"../lcres/aalc-{timestamp}.dot"

		# Create a mapping of nodes to their indices
		node_index_map = {node: str(i) for i, node in enumerate(GLC.nodes)}

		l_nodes_indices = [node_index_map[node] for node in GLC.nodes if node.startswith('l')]
		c_nodes_indices = [node_index_map[node] for node in GLC.nodes if node.startswith('c')]

		with open(dot_filename, "a") as f:
			f.write("strict graph G {\n")
			f.write("    graph [splines=true, nodesep=0.5, rankdir=TB];\n")
			f.write("    node [shape=circle, fixedsize=true, width=0.4, fontsize=10];\n")

			# Add nodes with indexed labels
			for node in GLC.nodes:
				node_type = GLC.nodes[node].get('type', "")
				node_card = GLC.nodes[node].get('card', "")
				#preceds = ",".join(map(str, GLC.nodes[node].get('preceds', [])))  # Join list if exists, else ""
				preceds = ",".join(node_index_map[p] for p in GLC.nodes[node].get('preceds', []) if p in node_index_map)
				index = node_index_map[node]  # Get index for the node
				#label = f"{node}#{index}"     # Create indexed label
				f.write(f'    {index} [label="{index}", type="{node_type}", preceds="{preceds}", realname="{node}", card="{node_card}"];\n')

			# Add edges
			for node_a, node_b in GLC.edges:
				index_a = node_index_map[node_a]  # Get index for node_a
				index_b = node_index_map[node_b]  # Get index for node_b
				f.write(f'    {index_a} -- {index_b} ;\n')


			f.write("}\n")
			print(f"DOT saved in :'{dot_filename}'")


	# Hypergraphe version Stell
	if affichage['HS']:
		plt.figure("HyperGraphe lignes/colonnes max")
		pos = nx.spring_layout(HST)
		labels_lignes = [n for n, d in HST.nodes(data=True) if d["type"] == "l"]
		node_sizes = [len(n) * 300 for n in labels_lignes]
		nx.draw_networkx_nodes(HST, pos, nodelist=labels_lignes, node_size=node_sizes,
						   node_color="lightgray", node_shape="s")
		labels_colonnes = [n for n, d in HST.nodes(data=True) if d["type"] == "c"]
		node_sizes = [len(n) * 300 for n in labels_colonnes]
		nx.draw_networkx_nodes(HST, pos, nodelist=labels_colonnes, node_size=node_sizes,
						   node_color="lightgray", node_shape="d")
		labels_tokens = [n for n, d in HST.nodes(data=True) if d["type"] == "t"]
		nx.draw_networkx_nodes(HST, pos, nodelist=labels_tokens, node_size=500,
						   node_color="lightgray", node_shape="o")

		nx.draw_networkx_edges(HST, pos, edge_color="black", arrowsize=20)
		nx.draw_networkx_labels(HST, pos, font_size=12, font_color="black")
		plt.savefig("HS.png")



if __name__ == '__main__':
	main()