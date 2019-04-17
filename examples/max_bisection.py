from graph import generate_rand_graph, Cut, print_adj
from algorithms.random_greedy import random_greedy
from algorithms.brute_force import brute_force
from util import get_mean
import networkx as nx
import matplotlib.pyplot as plt
import math


def main():
    graph_seed = 123
    algo_seed = None
    num_samples = 100

    k = 10
    n = 2 * k
    m = 30
    adj = generate_rand_graph(n, m, seed=graph_seed)
    cut_submod = Cut(adj)
    N = set(range(n))

    mode = 'normal'
    constraint = 'eq'
    print('Running Random Greedy')
    approx_val = get_mean(lambda: random_greedy(cut_submod, k,
                                                N, mode,
                                                constraint,
                                                seed=algo_seed)[1],
                          num_samples)

    print('Running Brute Force\n')
    opt = 15.066
    lower = opt * (1 - 1 / math.e)
    # opt = brute_force(cut_submod, k, N, constraint)
    # print('Approx OBJ:', approx_val)
    print('OPT:', opt)
    print('Lower bound:', lower)
    approx_set, _ = random_greedy(cut_submod, k, N, mode, constraint,
                                  seed=algo_seed)
    # print_adj(adj)
    g = nx.from_numpy_matrix(adj)
    node_color = []
    for node in g:
        if node in approx_set:
            node_color.append('red')
        else:
            node_color.append('black')
    edge_color = []
    for u, v in g.edges():
        if (u in approx_set and v not in approx_set) or (u not in approx_set
                                                         and v in approx_set):
            edge_color.append('blue')
        else:
            edge_color.append('black')
    nx.draw(g, node_color=node_color, edge_color=edge_color)
    plt.show()


if __name__ == '__main__':
    main()
