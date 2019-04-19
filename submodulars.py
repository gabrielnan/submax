from abc import ABC, abstractmethod
from random import random
import itertools
import numpy as np
import math
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


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
        for v in S:
            for u in self.N - S:
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
        assert u not in S

        marginal = 0
        for v in self.N:
            marginal += self.adj[u, v] * (-1 if v in S else 1)
        return marginal


class Dummy(Submodular):
    def __init__(self, submod, num_dummies):
        """
        Constructor

        :param self:
        :param submod: submodular function
        :return:
        """
        self.dummies = set([random() for _ in range(num_dummies)])
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


class Picture(Submodular):
    def __init__(self, img, w):
        self.img = img
        self.height, self.width, _ = img.shape
        super().__init__(set(itertools.product(range(self.height),
                                               range(self.width))))
        self.color_weight = w

    def dist(self, v, u):
        color_v = self.img[v]
        color_u = self.img[u]

        diff = np.array(v) - np.array(u)
        return self.color_weight * self.grey_dist(color_v, color_u) +\
               math.hypot(*diff)

    def grey_dist(self, color1, color2):
        return abs(self.rgb2grey(color1) - self.rgb2grey(color2))

    def rgb2grey(self, color):
        return (0.3 * color[0]) + (0.59 * color[1]) + (0.11 * color[2])

    def color_dist(self, color1, color2):
        color1_rgb = sRGBColor(*color1)
        color2_rgb = sRGBColor(*color2)

        color1_lab = convert_color(color1_rgb, LabColor)
        color2_lab = convert_color(color2_rgb, LabColor)

        # Find the color difference
        return delta_e_cie2000(color1_lab, color2_lab)

    def eval(self, S):
        S = S if isinstance(S, set) else set(S)
        cut = 0
        for v in S:
            for u in self.N - S:
                cut += self.dist(v, u)
        return cut

    def marginal(self, S, u):
        """
        Marginal cut value increase when adding u to S

        :param S: subset of V (iterable)
        :param u: vertex in V
        :return: marginal increase cut increase
        """
        S = S if isinstance(S, set) else set(S)
        assert u not in S

        marginal = 0
        for v in self.N:
            marginal += self.dist(u, v) * (-1 if v in S else 1)
        return marginal

