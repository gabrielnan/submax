import numpy as np
import random


def get_mean(fn, num_samples):
    sum = 0
    for i in range(num_samples):
        sum += fn()
    return sum / num_samples


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

