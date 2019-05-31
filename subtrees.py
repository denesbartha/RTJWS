from collections import defaultdict
from tree_labeling import get_labeled_graphs, gen_tree_from_list
from list_free_trees import listAllFreeTrees, gen_tree_edge_list_from_list, print_statistics
from sage.all import *
#sage/rings/polynomial/multi_polynomial_element.py
# turn off the warnings (because of sage)...
warnings.filterwarnings('ignore')
# introduce a new symbolic variable
x = sage.all.SR.var('x')
y = sage.all.SR.var('y')
sv = [x, y]



def subtree_r(d, t, v=0):
    if v in d:
        return d[v]
    elif v > 0 and len(t[v]) == 1:
        return 1
    rpol = 1
    for k in xrange(0 if v == 0 else 1, len(t[v])):
        rpol *= 1 + x * (subtree_r(d, t, t[v][k]))
    d[v] = rpol
    return d[v]


def subtree_f(d, t, v=0):
    s = subtree_r(d, t, v)
    for k in xrange(0 if v == 0 else 1, len(t[v])):
        s += subtree_f(d, t, t[v][k])
    return s

def subtree_large_unjumble(n):
    # d = defaultdict(int)
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        d[subtree_f({}, g).expand()].append(tuple(t))
        # d[subtree_f({}, g).expand()] += 1 #.append(tuple(t))
    return d

# print_statistics(3, 21, subtree_large_unjumble)


def subtree_labeled_r(d, edge_labels, labeling, t, v=0):
    if v in d:
        return d[v]
    elif v > 0 and len(t[v]) == 1:
        return 1
    rpol = 1
    for k in xrange(0 if v == 0 else 1, len(t[v])):
        rpol *= 1 + sv[labeling[edge_labels[(v, t[v][k])]]] * (subtree_labeled_r(d, edge_labels, labeling, t, t[v][k]))
    d[v] = rpol
    return d[v]


def subtree_labeled_f(d, edge_labels, labeling, t, v=0):
    s = subtree_labeled_r(d, edge_labels, labeling, t, v)
    for k in xrange(0 if v == 0 else 1, len(t[v])):
        s += subtree_labeled_f(d, edge_labels, labeling, t, t[v][k])
    return s


def subtree_small_unjumble(n):
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        for lbl in get_labeled_graphs(t, 2, True):
            # print subtree_labeled_f({}, edge_lbls, lbl, g).expand()
            # d[subtree_labeled_f({}, edge_lbls, lbl, g).expand()] += 1  # .append(tuple(t))
            d[subtree_labeled_f({}, edge_lbls, lbl, g).expand()].append((t, lbl))

    return d

# print_statistics(5, 6, subtree_small_unjumble)


def subtree_small_unjumble_weights(n):
    monomials = [[x**k * y**(i - k) for k in xrange(i + 1)] for i in xrange(1, n)]
    monomials_weights = [[1 * k + 2 * (i - k) for k in xrange(i + 1)] for i in xrange(1, n)]

    d = defaultdict(int)
    for t in listAllFreeTrees(n):
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        for lbl in get_labeled_graphs(t, 2, True):
            f = subtree_labeled_f({}, edge_lbls, lbl, g).expand()

            # wl = [ ]
            # for i in xrange(len(monomials)):
            #     wl.append(sum(f.coefficient(monomials[i][j])(x=0,y=0) * monomials_weights[i][j] for j in xrange(i + 2)))
            # print t, f.expand(), lbl
            wl = [0] * (sum(i + 1 for i in lbl) + 1)

            for i in xrange(len(monomials)):
                for j in xrange(i + 2):
                    # print monomials[i][j], f.coefficient(monomials[i][j]), f.coefficient(monomials[i][j])(x=0, y=0) * monomials_weights[i][j]
                    amonomial = f.coefficient(monomials[i][j])(x=0, y=0)
                    if amonomial != 0:
                        wl[monomials_weights[i][j]] += amonomial
            # print t, lbl, f, wl
            # d[tuple(wl)].append((t, lbl))
            d[tuple(wl)] += 1

    return d

print_statistics(3, 12, subtree_small_unjumble_weights)