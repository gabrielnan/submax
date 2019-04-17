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

    def unreduce(self, S):
        """
        Unreduces solution

        :param S: subset solution
        :return: unreduced subset for solution of original problem
        """
        return S

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


class Cut(Submodular):
    def __init__(self, adj):
        """
        Constructor

        :param adj: adjacency matrix
        """
        self.n = len(adj)
        super().__init__(set(range(self.n)))
        self.adj = adj
        self.cut_cache = dict()
        self.marginal_cache = dict()

    def eval(self, S):
        S = S if isinstance(S, set) else set(S)
        cut = 0
        for v in range(self.n):
            for u in range(v + 1, self.n):
                if (v in S and u not in S) or (v not in S and u in S):
                    cut += self.adj[u, v]
        return cut

    def marginal(self, S, u):
        """
        Marginal cut value increase when adding u to S

        :param S: subset of V (iterable)
        :param u: vertex in V
        :return: marginal increase cut increase
        """
        S = S if isinstance(S, set) else set(S)
        marginal = 0
        for v in range(self.n):
            if v in S:
                marginal -= self.adj[u, v]
            else:
                marginal += self.adj[u, v]
        return marginal


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
        S = S if isinstance(S, set) else set(S)
        return self.submod.eval(S - self.dummies)

    def marginal(self, S, u):
        if u in self.dummies:
            return 0
        S = S if isinstance(S, set) else set(S)
        return self.submod.marginal(S - self.dummies, u)

    def unreduce(self, S):
        return S - self.dummies


class Complement(Submodular):
    def __init__(self, submod):
        super().__init__(submod.universe())
        self.submod = submod

    def eval(self, S):
        return self.submod(self.N - S)

    def marginal(self, S, u):
        return - self.submod.marginal(u, S - {u})

    def unreduce(self, S):
        return self.N - S
