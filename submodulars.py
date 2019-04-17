from abc import ABC, abstractmethod


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


def Linear(Submodular):
    def __init__(self, weights):
        """
        Constructor

        :param weights: dict of element to weight
        """
        self.weights = weights
        self.N = set(weights.keys())

    def eval(self, S):
        sum = 0
        for u in S:
            sum += self.weights[u]
        return sum

    def marginal(self, S, u):
        assert u in S
        return self.weights[u]



