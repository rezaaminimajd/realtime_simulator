# import matplotlib.pyplot as plt
import networkx as nx
from random import random

from .GE import ge_edge, ge_nodes_count
from .FFT import fft_edge, fft_nodes_count
from .HEFT import calculate_heft


def generate_dags(dags_count, m, algorithm, processors_count):
    dags = {}
    for i in range(dags_count):
        dags[i] = create_tasks(m, algorithm, processors_count)
    return dags


def create_tasks(m, algorithm, processors_count):
    if algorithm == 'g':
        num_nodes = ge_nodes_count(m)
    else:
        num_nodes = fft_nodes_count(m)

    criticality = random()
    arrival_time = random() * 1000
    nodes = {}
    for i in range(num_nodes):
        nodes[i] = [int(10 + 90 * random()) for _ in range(processors_count)]
    if algorithm == 'g':
        G, edges = ge_edge(m, num_nodes, processors_count)
    else:
        G, edges = fft_edge(m, num_nodes, processors_count)
    dag = {
        'criticality': criticality,
        'arrival_time': arrival_time,
        'nodes': nodes,
        'edges': edges,
        'object': G
    }
    return dag


def show_dag(graph):
    plt.figure(figsize=(8, 6))
    nx.draw(
        graph,
        with_labels=True,
        node_color='lightblue',
        node_size=500,
        font_size=10,
        font_weight='bold',
        arrowstyle='->',
        arrowsize=10
    )
    plt.title("Random Directed Acyclic Graph")
    plt.show()


def generate(processors_count: int, lower_bound_factor: float):
    d, m = list(map(int, input("input number of dags and m parameter with space: ").split()))
    a = input("choose the generator algorithm (g: GE, f: FFT): ")
    s = input("do you want to show dag: (y: yes, n: no): ")
    dags = generate_dags(d, m, a, processors_count)
    for d in dags.values():
        lower_bound = calculate_heft(d)
        d['lower_bound'] = lower_bound * lower_bound_factor + d['arrival_time']
        if s == 'y':
            show_dag(d['object'])
    print(dags)
    return dags
