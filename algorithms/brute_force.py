from itertools import combinations
from scipy.misc import comb
from tqdm import tqdm


def brute_force(f, k, N, constraint):
    if constraint == 'eq':
        return brute_force_eq(f, k, N)
    elif constraint == 'leq':
        max_val = 0
        for i in range(k + 1):
            val = brute_force_eq(f, i, N)
            if val >= max_val:
                max_val = val
        return max_val


def brute_force_eq(f, k, N):
    max_val = 0
    for S in tqdm(combinations(N, k)):
        val = f.eval(S)
        if val >= max_val:
            max_val = val
    return max_val
