from enum import Enum, auto
from pycsp3 import *
import subprocess
import openpyxl
import re
import argparse
from datetime import datetime 
import os
import sys
import argparse
import pygraphviz as pgv
from pathlib import Path
import inflect
import networkx as nx
import pydot
from collections import Counter
from class_label_order import LabelOrder
from class_node import Node
from ilf import get_label,hopcroft, build_partial_order_3, build_partial_order_4,hopcroft_multiset,dir_ILF
#from digraph import graph_generator

#ilf=True

# Load data in model
def load(instance, graph_file, id, node_dict={}):
	
	# Load graph
	graph = nx.drawing.nx_agraph.read_dot(graph_file).to_directed()

	# Plot input graph
	pydot.graph_from_dot_file(graph_file)[0].write_png(f'res/{Path(os.path.basename(graph_file)).stem}.png')

	#print("Parsed nodes:", graph.nodes(data=True))

	#edges = graph.edges
	edges = [(u, v, d['angle']) for u, v, d in graph.edges(data=True) if 'angle' in d]
	labels = nx.get_node_attributes(graph, 'label')
	angles = nx.get_edge_attributes(graph, 'angle')
	graphs = pydot.graph_from_dot_file(graph_file)
	pydot_graph = graphs[0]
	nodes = pydot_graph.get_nodes()
	#print("Total nodes in PyDot:", len(nodes))
	#print("Node labels:", labels)

	# Set instance data
	instance[f'NV_{id}'] = graph.number_of_nodes()
	instance[f'NE_{id}'] = graph.number_of_edges()
	instance[f'V{id}'] = [label for label in labels.values()]
	instance[f'E{id}'] = list()
	instance[f'A{id}'] = list()

	for n1, n2, a in edges:
		instance[f'E{id}'].append((int(n1), int(n2)))
		key = (n1, n2, 0) if (n1, n2, 0) in angles else (n1, n2)
		instance[f'A{id}'].append('Horizontal' if angles[key] == '0' else 'Vertical')



def process_mapping( instance, mapping_n, mapping, target,pattern):

	print(f'{mapping_n}.\t[{", ".join(instance["V1"])}] -> [{", ".join(list(map(lambda i: instance["V2"][i], mapping)))}]')

	# Plot mapping
	graph = pydot.graph_from_dot_file(f'dat/{target}.dot')[0]
	for v1 in range(instance['NV_1']):
		graph.get_node(str(mapping[v1]))[0].set_label(instance['V1'][v1])
		graph.get_node(str(mapping[v1]))[0].set_style('filled')
	graph.write_png(f'res/{pattern}_in_{target}_{mapping_n}.png')


# Angle of the edge of a graph
class Angle(str, Enum):
	Horizontal = 'Horizontal'
	Vertical = 'Vertical'

def domain_n(i):
	if ilf:
		return node_dict[f'{i}p']
	else:
		return range(NV_2 )
def model(

	# =============== DATA
	
	#dom: list[str],
	# Pattern graph G1 = (V1, E1), with |V1| = NV_1, |E1| = NV_1, and A1 the angle of each edges in E1
	NV_1: int, 
	NE_1: int, 
	V1: list[str],
	E1: list[list[int]],
	A1: list[Angle],

	# Target graph G2 = (V2, E2), with |V2| = NV_2, |E2| = NV_2, and A2 the angle of each edges in E2
	NV_2: int, 
	NE_2: int, 
	V2: list[str],
	E2: list[list[int]],
	A2: list[Angle]
):


	# =============== VARIABLE

	# Mapping nodes from graph 1 to graph 2
	if ilf:
		I = VarArray(size=NV_1, dom=domain_n)
	else:
		I = VarArray(size=NV_1, dom=range(NV_2 ))
	T = {( i , j ) for i , j in E2 } | {( j , i ) for i , j in E2 }

	# =============== CONSTRAINT

	satisfy(

		AllDifferent(I),

		[
		Exist(
		(I[E1[e1][0]] == E2[e2][0]) & (I[E1[e1][1]] == E2[e2][1])
		for e2 in range(NE_2) if A1[e1]==A2[e2]
		) for e1 in range(NE_1)
		],

		[
		#((disjunction(I[n1] == node_dict[f'{n1+1}p'][i % len(node_dict[f'{n1+1}p'])])for i in range(len(node_dict[f'{n1+1}p'])) )for n1 in range(NV_1))
		#((I[n1] in node_dict[f'{n1+1}p'])for n1 in range(NV_1))
		]
	)
	# for i in range(NV_1):
	# 	print(I[i].dom)
	# print(posted())
	return I





if __name__ == '__main__':

	#pattern='dipan'
	#pattern='diWellFormed'
	# pattern='diNet'
	# # pattern='gap'
	
	# target='apositions-10032025130739'

	#python disip.py --pattern pan --target GLCRed --ilf 

	# parser = argparse.ArgumentParser(description='Process graph matching parameters.')
	# parser.add_argument('--pattern', type=str, required=True, help='Name of the pattern file (without .dot extension)')
	# parser.add_argument('--target', type=str, required=True, help='Name of the target file (without .dot extension)')
	# parser.add_argument('--ilf', action='store_true', help='Enable ILF option')
	# parser.add_argument('--ordre', action='store_true', help='Enable order option')
	# parser.add_argument('--typage', action='store_true', help='Enable typing option')

	# args = parser.parse_args()

	# pattern = args.pattern
	# target = args.target
	# ilf = args.ilf
	# ordre = args.ordre
	# typage = args.typage


	pattern = 'gap'
	target = 'apositions-10032025130739'
	target= 'apositions-11032025164627'
	ilf = False
	ordre = False
	typage = False
	card= False

	solver = ACE
	# Go to parent directory
	os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/..')
	print(os.path.dirname(os.path.realpath(__file__))+ '/..') 
	# Create a solving instance of the model
	instance = dict()


	Gp = nx.drawing.nx_agraph.read_dot(f'dat/{pattern}.dot')
	Gt = nx.drawing.nx_agraph.read_dot(f'dat/{target}.dot')
	Gp = nx.relabel_nodes(Gp, {node: f"{node}p" for node in Gp.nodes()})
	
	

	if ilf:
		node_list = dir_ILF(Gp,Gt)
		node_dict = {node._name: [int(value) for value in node._domain] for node in node_list if node._ispattern}
	else:
		node_dict = {}
	# Load data to the instance
	load(instance, f'dat/{pattern}.dot', 1, node_dict)
	load(instance, f'dat/{target}.dot', 2)

	I = model(**instance)

	result = solve(sols=ALL)
	
	ace_jar_path = "/home/etud/Bureau/projet/lib/python3.11/site-packages/pycsp3/solvers/ace/ACE-2.3.jar"

	# Run ACE solver directly using subprocess
	command = ["java", "-jar", ace_jar_path, "disip.xml", "-s=all", "-trace"]
	result = subprocess.run(command, capture_output=True, text=True)
	
	
	##EXCEL#################################################################################
	solver_output = result.stdout
	# Define regex pattern to extract indicators
	pattern1 = re.compile(r"dpts:(\d+\.\.\d+)?\s*effs:(\d+)?\s*(fails:(\d+))?\s*(wrgs:(\d+))?\s*wck:(\d+\.\d+)?\s*(ngds:(\d+))?\s*sols:(\d+)?")
	matches = pattern1.findall(solver_output)
	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "Indicators"


	
	headers = ["Run", "Dpts", "Effs", "Fails", "Wrgs", "Wck", "Ngds", "Sols"]
	ws.append(headers)

	# Write extracted data to Excel and add timestamp to each row
	run_count = 1  # To generate run numbers since "run" is missing in this format
	for match in matches:
		# Replace empty or missing values with "-"
		dpts = match[0] if match[0] else "-"
		effs = match[1] if match[1] else "-"
		fails = match[3] if match[3] else "-"
		wrgs = match[5] if match[5] else "0"
		wck = match[6] if match[6] else "-"
		ngds = match[8] if match[8] else "-"  # match[8] is for ngds (optional)
		sols = match[9] if match[9] else "0"

		# Append data to the Excel sheet
		row = [f"run{run_count}", dpts, effs, fails, wrgs, wck, ngds, sols]
		ws.append(row)
		run_count += 1

	# If no matches were found, execute the else block
	else:
		if not matches:  # Ensures the message only appears when the list is empty
			print("No indicator data found in the solver output.")

	# Append additional data outside the loop
	additional_data = ["Pattern", "Target", "ILF", "Order", "Typing"]  # Headers
	ws.append(additional_data)
	ws.append([pattern, target, ilf, ordre, typage])  # Values

	# Save the Excel file after processing all matches
	try:
		timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
		file_name = f"/home/etud/Bureau/projet/indicators_{timestamp}.xlsx"
		wb.save(file_name)
		print(f"Data has been written to {file_name}")
	except Exception as e:
		print(f"Error saving file: {e}")



	# Print the solver's output (including trace)
	print("Solver Output:")
	print(result.stdout) 
	print("Solver Error Output:")
	print(result.stderr)  
	num_solutions = n_solutions() or 0  # Default to 0 if None

	if num_solutions > 0:
		message=f'Patterns {pattern} in  {target}:'
		message += ' with ilf' if ilf else ' without ilf'
		print(message)
		for solution_i in range(n_solutions()):
			process_mapping( instance, solution_i + 1, values(I, sol=solution_i),target,pattern)
	else:
		message= 'sip: No solutions found :('
		message += ' with ilf' if ilf else ' without ilf'
		print(message) 