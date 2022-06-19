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





def print_tree_dot(file, tree, ops=None, numbers=None):
    assert( (not ops and not numbers) or len(ops) + 1 == len(numbers))

    dot_op_attrs = "shape=square"
    dot_leaf_attrs = "shape=circle"


    nodes_strs = ""
    link_strs = ""
    stack = [(tree,None)]

    count = 0
    while(len(stack) > 0):
        top, parent = stack.pop()
        name = f"node_{count}"
        count +=1
        if (parent):
            link_strs+=f"{parent}--{name}\n"

        attrs = ""
        label = "label= \"\""
        if (top == ()):
            attrs = dot_leaf_attrs
        else:
            attrs = dot_op_attrs
            stack.append((top[0], name))
            stack.append((top[1], name))

        nodes_strs += f"{name}[{attrs} {label}]\n"


    with open(file, "w") as f:
        f.write("graph G{\n")
        f.write(nodes_strs)
        f.write(link_strs)
        f.write("}\n")



c = 0
for tree in get_all_fbtrees(3):
    print_tree_dot(f"tree{c}.dot", tree)
    c +=1





