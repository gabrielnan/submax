from abc import ABC, abstractmethod
from random import random


class Submodular(ABC):
    def __init__(self, N):
        self.N = N

    @abstractmethod
    def eval(self, S):
        """
        Evalutes submodular function value at
        :param S:
        :return:
        """

    @abstractmethod
    def marginal(self, S, u):
        """
        Gets marginal of adding u to S
        :param S:
        :param u:
        :return:
        """
        return

    def universe(self):
        """
        Gets universal set
        :return: universal set
        """
        return self.N

    def __len__(self):
        return len(self.N)


class Linear(Submodular):
    def __init__(self, weights):
        """
        Constructor

        :param weights: dict of element to weight
        """
        super().__init__(set(weights.keys()))
        self.weights = weights

    def eval(self, S):
        sum = 0
        for u in S:
            sum += self.weights[u]
        return sum

    def marginal(self, S, u):
        assert u in S
        return self.weights[u]


class Dummy(Submodular):
    def __init__(self, submod, num_dummies):
        """
        Constructor

        :param self:
        :param submod: submodular function
        :return:
        """
        self.dummies = set([random() for _ in num_dummies])
        super().__init__(self.dummies.union(submod.universe()))
        self.submod = submod

    def eval(self, S):
        return self.submod.eval(S - self.dummies)

    def marginal(self, S, u):
        if u in self.dummies:
            return 0
        return self.submod.marginal(S - self.dummies, u)


class Cut(Submodular):
    def __init__(self, adj):
        self.n = len(adj)
        super().__init__(set(range(self.n)))
        self.adj = adj
        self.cut_cache = dict()
        self.marginal_cache = dict()

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
