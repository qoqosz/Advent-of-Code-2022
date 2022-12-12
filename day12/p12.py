import networkx as nx
import numpy as np


def neighbors(point):
    """2D neighboring points."""
    for i in (-1, 1):
        yield (point[0] + i, point[1])
        yield (point[0], point[1] + i)


def build_graph(arr):
    """
    arr - input heightmap
    x - value (char) in arr
    p = it.multi_index - coordinates of x
    n - coordinates of x's neighbors
    """
    G = nx.DiGraph()
    it = np.nditer(arr, flags=['multi_index'])

    for x in it:
        p = it.multi_index
        x_val = str(x)

        for n in neighbors(p):
            try:
                n_val = str(arr[n])
            except IndexError:
                continue

            if n >= (0, 0):
                if x_val == 'S' or n_val == 'S':
                    G.add_edge(p, n)

                if x_val == 'E' and n_val in ('y', 'z'):
                    G.add_edge(p, n)

                if x_val in ('y', 'z') and n_val == 'E':
                    G.add_edge(p, n)

                if ord(x_val) + 1 >= ord(n_val):
                    G.add_edge(p, n)
    return G


def path_len(G, start, end):
    return len(nx.shortest_path(G, start, end)) - 1


with open('p12.txt') as f:
    heightmap = np.array([[c for c in row.strip()] for row in f.readlines()])

start = tuple(map(int, np.where(heightmap == 'S')))
end = tuple(map(int, np.where(heightmap == 'E')))

# Part I
G = build_graph(heightmap)
print(path_len(G, start, end))

# Part II
lens = []

for start in [(a, b) for a, b in zip(*np.where(heightmap == 'a'))]:
    try:
        lens.append(path_len(G, start, end))
    except Exception:
        continue

print(min(lens))
