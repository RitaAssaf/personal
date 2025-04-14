
('1', '2'):
'c'
('1', '4'):
'l'
('2', '3'):
'l'
('3', '4'):
'c'
('4', '5'):
'l'


cnt = 0
while solve () is SAT :
cnt += 1
print ( f " Solution { cnt }:satisfy ( x != values ( x ))
{ 

before it was n1,n2 integers in E1 array of edges and constraint was:
  Or(
                (I[E1[e][0]], I[E1[e][1] ]) in E2,
                (I[E1[e][1] ], I[E1[e][0]]) in E2 #bidirection  2 sens e.g. 1--4 4---1
            )
            
            
for edge in E1:
            print(f"Order of edge {edge}: {O1[edge]}")
            
            
E1 aretes du graphe G1 (pan):
 les noeus sont 1,2,3,4,5 donc E1[e][0]
 
 mais on doit les convertir
     E = [(int(n1), int(n2)) for n1, n2 in edges]
     
   I = VarArray(size=NV_1, dom=range(1, NV_2 + 1))

    # ===== CONSTRAINTS =====
    satisfy(
     
        AllDifferent(I),

  
        [
            Or(
                (I[E1[e][0]-1], I[E1[e][1]-1 ]) in E2 
            )
            for e in range(NE_1)
        ]
    )



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
    #E = [(n1, n2) for n1, n2 in edges]
    E = [(int(n1), int(n2)) for n1, n2 in edges]
    
    return NV, NE, V, E, O


NV_1, NE_1, V1, E1, O1 = load("pattern.dot") # pattern = pan
NV_2, NE_2, V2, E2, O2 = load("target.dot")  # target = network

if NV_1 > 0 and NV_2 > 0:
    # ===== VARIABLES =====
    
    #for edge in E1:
     #       print(f"Order of edge {edge}: {O1[edge]}")

    I = VarArray(size=NV_1, dom=range(1, NV_2 + 1))

    # ===== CONSTRAINTS =====
    satisfy(
     
        AllDifferent(I),

  
        [ Or(
                (I[E1[e][0]-1], I[E1[e][1] -1]) in E2,
                (I[E1[e][1] -1], I[E1[e][0]-1]) in E2 #bidirection  2 sens e.g. 1--4 4---1
            )for e in range(NE_1)
            
        ]
    )

    # ===== SOLVE =====
    cnt = 0
    while solve () is SAT :
        cnt += 1
        print(f" Solution { cnt }:{ values ( I )} " )
        satisfy ( I != values ( I))
  
  
  
  
        [ Or(
                (I[E1[e][0]-1], I[E1[e][1] -1]) in E2
                ,(I[E1[e][1] -1], I[E1[e][0]-1]) in E2 #bidirection  2 sens e.g. 1--4 4---1
            )for e in range(NE_1)
            
        ]
        
        
  [
            if_then(
                Or(
                    (I[u - 1], I[v - 1]) == edge2,
                    (I[v - 1], I[u - 1]) == edge2
                ),
                O1[edge1] == O2[edge2]
            )
            for edge1 in E_o1
            for edge2 in E_o2
        ]
        
        
         [ Or(
                (I[E1[e][0]-1], I[E1[e][1] -1]) in E2
                ,(I[E1[e][1] -1], I[E1[e][0]-1]) in E2 #bidirection  2 sens e.g. 1--4 4---1
            )for e in range(NE_1) >> 
         
           (O1[edge1] == O2[edge2]
            )
            for edge1 in E_o1
            for edge2 in E_o2
            
        ]



             satisfy(
        # Ensure all vertices in the pattern graph map to different vertices in the target graph
        AllDifferent(I),

        # Ensure edges in the pattern graph map to edges in the target graph
        [
            Or(
                (I[E1[e][0] - 1], I[E1[e][1] - 1]) in E2,  # Direction 1
                (I[E1[e][1] - 1], I[E1[e][0] - 1]) in E2   # Direction 2
            )
            for e in range(NE_1)
        ]
    )



