import numpy as np
import random
import os

TOP_DIR = os.path.dirname(os.path.realpath(__file__))


def get_stats(fn, num_samples):
    vals = np.array([fn() for _ in range(num_samples)])
    return vals.mean(), vals.max(), vals.std()


def generate_rand_graph(n, m, seed=None):
    """
    Generates a connected graph with n vertices and m edges

    :param n: number of vertices
    :param m: number of edges
    :return: adjacency matrix
    """
    random.seed(seed)
    adj = np.zeros([n, n])
    for v in range(1, n):
        u = random.randint(0, v - 1)
        adj[u, v] = adj[v, u] = random.random()

    num_edges = n - 1
    while num_edges < m:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and adj[u, v] == 0:
            adj[u, v] = adj[v, u] = random.random()
            num_edges += 1
    return adj


def print_adj(adj):
    n = len(adj)
    for i in range(n):
        print(', '.join((adj[i] > 0).astype(int).astype(str)))

