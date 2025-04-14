import os
import sys
import argparse
from pathlib import Path

import networkx as nx
import pydot
from minizinc import Model, Solver, Instance

# Load data in model
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

if __name__ == '__main__':

	# Parse command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--pattern', type=str, default='pan', help='Pattern graph')
	parser.add_argument('-t', '--target', type=str, default='net', help='Target graph')
	parser.add_argument('-a', '--all', action=argparse.BooleanOptionalAction, default=False, help='Get all solutions')
	args = parser.parse_args()

	# Go to parent directory
	os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/..')

	# Find the MiniZinc solver configuration for Gecode with globals dir
	solver = Solver.lookup('gecode')

	# Load SIP model from file
	model = Model('src/sip.mzn')

	# Create a solving instance of the model
	instance = Instance(solver, model)

	# Load data to the instance
	load(instance, f'dat/{args.pattern}.dot', 1)
	load(instance, f'dat/{args.target}.dot', 2)

	# Solve the instance
	results = instance.solve(verbose=True, all_solutions=args.all, debug_output=Path(f'res/{args.pattern}_in_{args.target}.txt'))

	# Output the result
	if results.status.has_solution():

		# Print mapping
		print(f'Patterns {args.pattern} in target {args.target}:')
		solution_number = 1
		for result in results:
			print(f'- [{", ".join(instance["V1"])}] -> [{", ".join(list(map(lambda i: instance["V2"][i-1], result.I)))}]')

			# Plot mapping
			graph = pydot.graph_from_dot_file(f'dat/{args.target}.dot')[0]
			for v1 in range(instance['NV_1']):
				graph.get_node(str(result.I[v1]))[0].set_label(instance['V1'][v1])
				graph.get_node(str(result.I[v1]))[0].set_style('filled')
			graph.write_png(f'res/{args.pattern}_in_{args.target}_{solution_number}.png')
			solution_number += 1
	
	else:
		print(f'{result.status}')