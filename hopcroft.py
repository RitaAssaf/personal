import networkx as nx

# Function to check if m <= m' using Hopcroft-Karp algorithm
def multiset_comparison_hopcroft(m, m_prime):
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

# Example multisets
m = [6,8]
m_prime = [2, 3, 5, 5]

# Compare multisets using Hopcroft-Karp
result = multiset_comparison_hopcroft(m, m_prime)

if result:
    print(f"Multiset {m} <= {m_prime}")
else:
    print(f"Multiset {m} is not comparable to {m_prime}")
