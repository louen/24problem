import itertools
import numpy as np

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
    """Print a tree in the dot format for display with optionnal asignment"""
    assert( (not ops and not numbers) or len(ops) + 1 == len(numbers))

    dot_op_attrs = "shape=square"
    dot_leaf_attrs = "shape=circle"


    nodes_strs = ""
    link_strs = ""

    op_count = 0
    num_count = 0

    # Traverse the tree with a stack of (current node, parent name)
    stack = [(tree,None)]
    while stack:
        top, parent = stack.pop()
        count = op_count + num_count
        name = f"node_{count}"
        if (parent):
            link_strs+=f"{parent}--{name}\n"

        attrs = ""
        label = "\"\""
        if (top == ()):
            attrs = dot_leaf_attrs
            if (numbers):
                label=f"\"{numbers[num_count]}\""
            num_count +=1
        else:
            attrs = dot_op_attrs
            # Reverse order for tree traversal
            stack.append((top[1], name))
            stack.append((top[0], name))

            if (ops):
                label=f"\"{ops[op_count]}\""
            op_count +=1

        nodes_strs += f"{name}[{attrs} label={label}]\n"


    with open(file, "w") as f:
        f.write("graph G{\n")
        f.write(nodes_strs)
        f.write(link_strs)
        f.write("}\n")

def get_expr_string(tree, ops=None, numbers=None):
    """return the expression corresponding to a given tree as a string"""
    assert( (not ops and not numbers) or len(ops) + 1 == len(numbers))
    
    result =""
    op_count = 0
    num_count = 0

    # Traverse the tree with a stack of nodes and extra strings to insert 
    stack = [tree]
    while stack:
        top = stack.pop()
        if top == () and numbers:
            result += numbers[num_count]
            num_count +=1
        elif isinstance(top, str):
            result += top
        else:
            # Add to the stack in reverse order
            result += "("
            stack.append(")")
            stack.append(top[1])
            if ops:
                stack.append(ops[op_count])
                op_count +=1
            stack.append(top[0])

    return result


   
def print_polygon_dot(file, tree, ops=None, numbers=None):
    """Print the corresponding polygon triangulation to the given tree"""


    def polygon_tree_rec(tree, vc, oc, ops, numbers):
        if (tree == ()):
            return ((),[vc,vc+1], numbers[vc] if numbers else ""),  vc+1, oc
        else:
            lt,vc,oc = polygon_tree_rec(tree[0],vc, oc, ops, numbers)
            rt,vc,oc = polygon_tree_rec(tree[1],vc, oc, ops, numbers)
            string = "("+lt[2]+ops[oc] + rt[2]+")" if ops else ""
            return ((lt,rt),[lt[1][0], rt[1][1]], string), vc, oc+1

    edge_str = ""
    vertex_str = ""


    # First, traverse the tree recursively and populate the edges
    edge_tree, _,_ = polygon_tree_rec(tree,0,0,ops,numbers)
    edge = edge_tree[1]

    assert( (not ops and not numbers)  or ((len(ops) + 1 == len(numbers)) and len(numbers) == edge[1]))

    # Create all needed vertices
    N = edge[1] +1
    for i in range(N):
        x = np.cos(2*i*np.pi/N)
        y = np.sin(2*i*np.pi/N)
        vertex_str += f"v{i}  [pos=\"{x},{y}!\"]\n"

    # Stack traversal of the edge tree and evaluate labels if needed 
    stack = [edge_tree]
    while stack:
        struct,edge,string = stack.pop()
        label = ""
        if numbers and ops:
            label = f"[label=\"{string}\"]"
        if struct !=():
            stack.append(struct[1])
            stack.append(struct[0])

        edge_str += f"v{edge[0]} -- v{edge[1]} "+ label +"\n"
        
    # add final edge representing the whole expr

    with open(file,"w") as f:
        f.write("graph G {\n")
        f.write(f"layout=neato\nnormalize={360.0/N}\nnode[shape=point]\n")
        f.write(vertex_str +"\n")
        f.write(edge_str)
        f.write("}\n")







c = 0
for tree in get_all_fbtrees(3):
    print_tree_dot(f"tree{c}.dot", tree,[".",".","."],["a","b","c","d"])
    print_polygon_dot(f"tree{c}pent.dot", tree,[".",".","."],["a","b","c","d"])
    print_polygon_dot(f"tree{c}pent.dot",tree)
    c +=1
    #print(str(tree) +" " +get_expr_string(tree,[".",".","."],["a","b","c","d"]))





