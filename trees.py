import itertools

from timeit import default_timer as timer

def get_all_fbtrees_rec(n):
    """Return a list of all possible full binary trees with exactly n internal
    nodes and n+1 leaves, as nested tuples. Recursive version."""
    # base case, single leaf
    if (n == 0):
        return [()]
    trees = []
    # for all possible splits between left and right
    for i in range(n):
        left_subtrees = get_all_fbtrees_rec(i)
        right_subtrees = get_all_fbtrees_rec(n-i-1)
        # for all possible combination of left and right subtrees
        for l,r in itertools.product(left_subtrees, right_subtrees):
              trees.append((l,r))
    return trees


def get_all_fbtrees(n):
    """Return a list of all possible full binary trees with exactly n internal
    nodes and n+1 leaves, as nested tuples. Iterative faster version."""
    # Build the list of all possible trees as k increase, memorizing the answers
    trees_memo = [[()]]
    for k in range(1,n+1):
        trees = []
        for i in range(k):
            left_subtrees = trees_memo[i]
            right_subtrees = trees_memo[k-i-1]
            for l,r in itertools.product(left_subtrees, right_subtrees):
                trees.append((l,r))
        trees_memo.append(trees)

    return trees_memo[-1]
    


# tests
for i in range(16):
    t0 = timer()
    n = len(get_all_fbtrees_rec(i))
    t1 = timer()
    print(f"{i} : {n} - {t1 - t0}s")


for i in range(16):
    t0 = timer()
    n = len(get_all_fbtrees(i))
    t1 = timer()
    print(f"{i} : {n} - {t1 - t0}s")






