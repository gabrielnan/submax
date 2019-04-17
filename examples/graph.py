import numpy as np
import random
from submodulars import Submodular


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


class Cut(Submodular):
    def __init__(self, adj):
        self.adj = adj
        self.cut_cache = dict()
        self.marginal_cache = dict()
        self.n = len(adj)

    def eval(self, S):
        # if S in self.cut_cache:
        #     return self.cut_cache[S]
        S = S if isinstance(S, set) else set(S)
        cut = 0
        for v in range(self.n):
            for u in range(v + 1, self.n):
                if (v in S and u not in S) or (v not in S and u in S):
                    cut += self.adj[u, v]
        # self.cut_cache[S] = cut
        return cut

    def marginal(self, S, u):
        """
        Marginal cut value increase when adding u to S

        :param S: subset of V (iterable)
        :param u: vertex in V
        :return: marginal increase cut increase
        """
        # if (S, u) in self.marginal_cache:
        #     return self.marginal_cache[(S, u)]
        S = S if isinstance(S, set) else set(S)
        marginal = 0
        for v in range(self.n):
            if v in S:
                marginal -= self.adj[u, v]
            else:
                marginal += self.adj[u, v]
        # self.marginal_cache[(S, u)] = marginal
        return marginal


class Graph:
    def __init__(self, adj):
        self.n = len(adj)
        self.adj = adj
        self.V = set(range(self.n))
        self.cut = Cut(self.adj)

    def cut(self, S):
        cut = 0
        for v in self.V:
            for u in range(v + 1, self.n):
                if (v in S and u not in S) or (v not in S and u in S):
                    cut += self.adj[u, v]
        return cut

    def marginal_cut(self, S, u):
        """
        Marginal cut value increase when adding u to S

        :param S: subset of V
        :param u: vertex in V
        :return: marginal increase cut increase
        """
        cut = 0
        for v in self.V:
            if v in S:
                cut -= self.adj[u, v]
            else:
                cut += self.adj[u, v]
        return cut
