import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.cm import ScalarMappable
import numpy as np

n = 15  # number of nodes
eps = 0.1
radius = (1-eps)*np.sqrt(np.log(n)/n)  # radius for edge connection

# generate nodes with random positions in [0,1]x[0,1]
pos = {i: (random.random(), random.random()) for i in range(n)}

# create graph and add nodes
G = nx.Graph()
G.add_nodes_from(range(n))

# add edges between nodes within the radius
for i in range(n):
    for j in range(i+1, n):
        dist = ((pos[i][0]-pos[j][0])**2 + (pos[i][1]-pos[j][1])**2)**0.5
        if dist <= radius:
            weight = random.uniform(0, 1)  # add random uniform weight to edge
            G.add_edge(i, j, weight=weight)

# get edge weights
edge_weights = [G[i][j]['weight'] for i, j in G.edges()]

# set color map for edges
edge_cmap = plt.cm.get_cmap('YlOrRd')

# create a ScalarMappable object for edges
edge_norm = plt.Normalize(min(edge_weights), max(edge_weights))
edge_sm = ScalarMappable(norm=edge_norm, cmap=edge_cmap)

# visualize graph with edges colored according to their weights
nx.draw(G, pos, node_size=50, edge_color=edge_weights,
        edge_cmap=edge_cmap, width=2)
plt.colorbar(edge_sm)
plt.show()

# find longest increasing path


def increasing_path_length(path):
    """Return the total length of the path with increasing edge weights."""
    length = 1
    for i in range(len(path)-2):
        if G[path[i]][path[i+1]]['weight'] <= G[path[i+1]][path[i+2]]['weight']:
            length += 1
        else:
            length = 0
            break
    return length


paths = []

for i in range(n):
    for j in range(i+1, n):
        print("*** finding paths between {} and {} ***".format(i, j))
        if nx.has_path(G, i, j):
            for path in nx.all_simple_paths(G, i, j):
                paths.append(path)

paths = paths + [list(reversed(path)) for path in paths]
print(len(paths))

longest_path = max(paths, key=increasing_path_length)

# print longest path and its length
print("Longest path with increasing edge weights:", longest_path)
print("Length:", increasing_path_length(longest_path))
# print the edge weights of longest_path, truncate float to 3 decimal places
print("Edge weights:", [round(G[longest_path[i]][longest_path[i+1]]
      ['weight'], 3) for i in range(len(longest_path)-1)])
