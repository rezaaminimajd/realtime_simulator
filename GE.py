import networkx as nx
import numpy as np
from random import random


def ge_edge(m, num_nodes, processors_count):
    edges = {}
    G = nx.DiGraph()
    G.add_nodes_from(range(num_nodes))
    base = 0
    for i in range(m, 0, -1):
        for j in range(1, i):
            if base + j >= num_nodes:
                break
            G.add_edge(base, base + j)
            edges[base] = [(base + j, [int(5 + random() * 20) for _ in range(processors_count)])]
            # print(base, base + j)
        for j in range(1, i):
            if j + i - 1 + base >= num_nodes:
                break
            G.add_edge(j + base, j + i - 1 + base)
            edges[j + base] = [(j + i - 1 + base, [int(5 + random() * 20) for _ in range(processors_count)])]
            # print(j + base, j + i - 1 + base, j, i)
        base += i
    return G, edges


def ge_nodes_count(m):
    return int((m * m + m - 2) / 2)
