import random
import numpy as np
from tqdm import trange


def get_max_subset(f, S, big_set, k):
    """
    Gets subset of size k that maximizes sum_{u in
    :param f:
    :param S:
    :param big_set:
    :param k:
    :return:
    """

    marginals = []
    for u in big_set:
        marginals.append((u, f.marginal(S, u)))
    sorted_marginals = sorted(marginals, key=lambda elem: elem[1])
    return set([elem[0] for elem in sorted_marginals[:k]])


def reduce1(f, k, N):
    """
    Preprocess original universal set so that the size of new set is geq 2k
    :param f: submodular function
    :param N: original universal set
    :param k: k
    :return: tuple(corresponding submodular function, preprocessed set)

    """
    raise NotImplementedError('gotta implement this')


def reduce2(f, k, N):
    """
    Preprocess original universal set so that the size of new set is geq 2k
    :param f: submodular function
    :param N: original universal set
    :param k: k
    :return: tuple(corresponding submodular function, preprocessed set)
    """
    if len(N) >= 2 * k:
        return f, N
    else:
        raise NotImplementedError('implement this')


def wide_size(i, k):
    I = int(np.ceil(0.21 * k))
    if i <= I:
        return 2 * (k - i + 1)
    return k


def random_greedy(f, k, N, mode='normal', constraint='eq', seed=None):
    """

    :param f: Submodular object
    :param k: size of subset constraint
    :param N: universal set
    :param mode: either 'normal' or 'wide'
    :param constraint: either 'leq' or 'eq'
    :return:
    """
    random.seed(seed)
    if mode == 'normal':
        size_fn = lambda i: k
    elif mode == 'wide':
        size_fn = lambda i: wide_size(i, k)
    else:
        raise ValueError('mode is either normal or wide')

    if constraint == 'eq':
        reduce_fn = reduce2
    elif constraint == 'leq':
        reduce_fn = reduce1
    else:
        raise ValueError('constraint is either "leq" or "eq"')

    return _random_greedy(f, k, N, reduce_fn, size_fn)


def _random_greedy(f, k, N, reduce_fn, size_fn):
    """
    Runs random greedy algorithm. Assumes 2k <= |N|

    :param f: non-negative submodular function that takes in a subset of N
    and returns a real value
    :param k: max size of return set (cardinality
    constraint)
    :param N: universal set of elements
    :param size_fn: function that takes in integer and returns a size of
    subset to sample from
    :return: a subset of N, obj(soln)
    """

    f, N = reduce_fn(f, k, N)
    curr_set = set()
    curr_set_comp = N.copy()
    for i in trange(k):
        M = get_max_subset(f, curr_set, curr_set_comp, size_fn(i + 1))
        new_element = random.sample(M, 1)[0]
        curr_set.add(new_element)
        curr_set_comp.remove(new_element)
    return curr_set, f.eval(curr_set)


