from pycsp3 import *
import os
import networkx as nx
from pathlib import Path
import pydot


def load(graph_file):
    # Load graph
    graph = nx.drawing.nx_agraph.read_dot(graph_file)

    # Get graph edges and labels
    edges = graph.edges
    labels = nx.get_node_attributes(graph, 'label')
    O = nx.get_edge_attributes(graph, 'order')
    
    # Set instance data
    NV = graph.number_of_nodes()
    NE = graph.number_of_edges()
    V = [label for label in labels.values()]
    E_o = [(n1, n2) for n1, n2 in edges]
    E = [(int(n1), int(n2)) for n1, n2 in edges]
    
    return NV, NE, V, E, O, E_o


NV_1, NE_1, V1, E1, O1 , E_o1= load("pattern.dot") # pattern = pan
NV_2, NE_2, V2, E2, O2 , E_o2= load("target.dot")  # target = network

if NV_1 > 0 and NV_2 > 0:
    # ===== VARIABLES =====
    
    for edge in E_o1:
           print(f"Order of edge {edge}: {O1[edge]}")

    I = VarArray(size=NV_1, dom=range(1, NV_2 + 1))
  

    # ===== CONSTRAINTS =====
    satisfy(
     
        AllDifferent(I),

        [ Or(
                (I[E1[e][0]-1], I[E1[e][1] -1]) in E2
                ,(I[E1[e][1] -1], I[E1[e][0]-1]) in E2 #bidirection  2 sens e.g. 1--4 4---1
            )for e in range(NE_1)
            
        ],
        
      [
    If(
        (I[edge1[0] - 1], I[edge1[1] - 1]) in E2 or (I[edge1[1] - 1], I[edge1[0] - 1]) in E2,
        Then= O1[edge1] == O2[edge2]
    )
    for edge1 in E_o1
    for edge2 in E_o2
]
        
       
    )

    # ===== SOLVE =====
    cnt = 0
    while solve () is SAT :
        cnt += 1
        print(f" Solution { cnt }:{ values ( I )} " )
        satisfy ( I != values ( I))
  
    print("solve unsat")