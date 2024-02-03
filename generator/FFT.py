import networkx as nx
import numpy as np
from random import random


def fft_edge(m, num_nodes, processors_count):
    edges = {}
    G = nx.DiGraph()
    G.add_nodes_from(range(1, num_nodes))
    for i in range(1, int((2 ** (np.log2(m))))):
        G.add_edge(i, 2 * i)
        edges[i] = [(2 * i, [int(5 + random() * 20) for _ in range(processors_count)])]
        # print(i, 2 * i)
        G.add_edge(i, 2 * i + 1)
        edges[i] = [(2 * i + 1, [int(5 + random() * 20) for _ in range(processors_count)])]
        # print(i, 2 * i + 1)
    for i in range(m, num_nodes - m + 1):
        G.add_edge(i, i + m)
        edges[i] = [(i + m, [int(5 + random() * 20) for _ in range(processors_count)])]
        # print(i, i + m)
    for i in range(m, num_nodes - m + 1, 4):
        splitter = i // m
        start_index = splitter * m
        end_index = splitter * m + m
        for j in range(start_index, end_index):
            sign = np.power(-1, ((j - m) // splitter))
            G.add_edge(j, j + m + sign * splitter)
            edges[j] = [(j + m + sign * splitter, [int(5 + random() * 20) for _ in range(processors_count)])]
            # print(j, j + m + sign * splitter)

    new_edges = {}
    for k, v in edges.items():
        new_edges[k - 1] = [(v[0][0] - 1, v[0][1])]

    return G, new_edges


def fft_nodes_count(m):
    return int(m * np.log2(m) + 2 * m - 1)
