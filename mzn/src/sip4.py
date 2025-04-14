from pycsp3 import *

# ===== DATA =====
NV_1 = 4  # Number of vertices in graph 1
NE_1 = 3  # Number of edges in graph 1
V1 = ["A", "B", "C", "D"]  # Names of vertices in graph 1
E1 = [(1, 2), (2, 3), (3, 4)]  # Edges of graph 1 (1-indexed)

NV_2 = 5  # Number of vertices in graph 2
NE_2 = 4  # Number of edges in graph 2
V2 = ["W", "X", "Y", "Z", "T"]  # Names of vertices in graph 2
E2 = [(1, 2), (2, 3), (3, 4), (4, 5)]  # Edges of graph 2 (1-indexed)

# ===== VARIABLES =====
# I[i] is the vertex in graph 2 that vertex i of graph 1 is mapped to
I = VarArray(size=NV_1, dom=range(1, NV_2 + 1))

# ===== CONSTRAINTS =====
# 1. All nodes in graph 1 must be mapped to different nodes in graph 2
satisfy(
    AllDifferent(I)
)

# 2. Each edge of graph 1 must have a corresponding edge in graph 2
satisfy(
    [ 
        Or(
            (I[E1[e][0] - 1], I[E1[e][1] - 1]) in E2,
            (I[E1[e][1] - 1], I[E1[e][0] - 1]) in E2  # Since the graph is undirected
        )
        for e in range(NE_1)
    ]
)

# ===== SOLVE =====
satisfy()
