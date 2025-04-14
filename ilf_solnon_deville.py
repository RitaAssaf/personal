import networkx as nx
from collections import defaultdict, deque

def test_compatibility(multiset_u, multiset_v):
    # Sort both multisets to make matching easier
    multiset_u.sort()
    multiset_v.sort()

    # Try to match each element in multiset_u to an element in multiset_v
    i, j = 0, 0  # i for multiset_u, j for multiset_v

    while i < len(multiset_u) and j < len(multiset_v):
        if multiset_u[i] <= multiset_v[j]:
            # We found a match for multiset_u[i], move to the next element in both sets
            i += 1
        # Whether a match is found or not, move to the next element in multiset_v
        j += 1

    # If we were able to match all elements of multiset_u, return True
    return i == len(multiset_u)

# Problem parameters: Gp and Gt are the pattern and target graphs, Lvar is the set of CSP variables
def ILF(Gp, Gt, Lvar, D, k):
    np = len(Gp.nodes)  # number of nodes in pattern graph
    nt = len(Gt.nodes)  # number of nodes in target graph

    # Step 1: Initial labeling based on the degree of nodes
    labeling = {node: Gp.degree[node] for node in Gp.nodes}  # Initial labeling for pattern graph
    print(" labeling pattern:", labeling)

    # Ensure all target graph nodes also have labels based on their degree
    for node in Gt.nodes:
        labeling[node] = Gt.degree[node]  # Initial labeling for target graph
    print("0 labeling target:", labeling)

    for u in Gp.nodes:
        for v in Gt.nodes:
            if not labeling[u]<= labeling[v]:
                D[u].remove(v)

    for iteration in range(k):
        # Step 2: For each pattern node u, filter target nodes based on current labeling
        for u in Gp.nodes:
            neighbors_u = list(Gp.neighbors(u))
            D_u = D[u]
            print('u:',u, 'domain ', D_u)

            for v in list(D_u):
                neighbors_v = list(Gt.neighbors(v))
                multiset_u = [labeling[n] for n in neighbors_u]
                multiset_v = [labeling[n] for n in neighbors_v]

                # Apply the Hopcroft-Karp compatibility test between multisets of labels
                if not test_compatibility(multiset_u, multiset_v):
                    D[u].remove(v)  # Filter incompatible target node
                print('i: ', iteration, 'u: ', u, ' dom ', D[u])
        # Step 3: Update labeling using neighborhood extension
        new_labeling = {}
        for u in Gp.nodes:
            neighbors_u = list(Gp.neighbors(u))
            multiset_u = [labeling[n] for n in neighbors_u]
            new_labeling[u] = (labeling[u], multiset_u)

        # Ensure all target graph nodes also get updated labels in new_labeling
        for v in Gt.nodes:
            if v not in new_labeling:
                neighbors_v = list(Gt.neighbors(v))
                multiset_v = [labeling[n] for n in neighbors_v]
                new_labeling[v] = (labeling[v], multiset_v)

        labeling = new_labeling  # Update labeling for next iteration

       
    return D

 # Example usage for ILF (NetworkX graphs)
# Gp = nx.Graph([(0, 1), (1, 2)])  # Example pattern graph
# Gt = nx.Graph([(0, 1), (1, 2), (2, 3)])  # Example target graph
# Lvar = {0: 'x0', 1: 'x1', 2: 'x2'}  # Example CSP variables
# D = {0: {0, 1, 2,3}, 1: {0, 1, 2,3}, 2: {0, 1, 2,3}}  # Initial domain of variables 

# Example usage for ILF (NetworkX graphs)
# Example pattern graph Gp
Gp = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])  # Simple cycle

# Example target graph Gt, using string labels for nodes ('a', 'b', etc.)
Gt = nx.Graph([
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



# Apply ILF algorithm
filtered_D = ILF(Gp, Gt, Lvar, D, k=6)
print("Filtered domains after ILF:", filtered_D)
