import networkx as nx

# create graph
G = nx.Graph()
n, m = input().split()
for i in range(int(m)):
    u, v = input().split()
    u = int(u)
    v = int(v)
    G.add_edge(u, v)
print(list(nx.find_cliques(G)))
