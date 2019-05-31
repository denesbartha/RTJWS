from collections import defaultdict
from tree_labeling import get_labeled_graphs, gen_tree_from_list
from list_free_trees import listAllFreeTrees, gen_tree_edge_list_from_list, print_statistics
from sage.all import *

# turn off the warnings (because of sage)...
warnings.filterwarnings('ignore')
# introduce a new symbolic variable
x = sage.all.SR.var('x')
y = sage.all.SR.var('y')

sv = [x, y]

def path_r(d, t, v=0):
    if v in d:
        return d[v]
    elif v > 0 and len(t[v]) == 1:
        return 1
    rpol = 1
    for k in xrange(0 if v == 0 else 1, len(t[v])):
        rpol += x * (path_r(d, t, t[v][k]))
    d[v] = rpol
    return d[v]


def path_f(d, t, v=0):
    s = path_r(d, t, v)
    for i in xrange(0 if v == 0 else 1, len(t[v])):
        for j in xrange(i + 1, len(t[v])):
            s += x * x * path_r(d, t, t[v][i]) * path_r(d, t, t[v][j])

    for k in xrange(0 if v == 0 else 1, len(t[v])):
        s += path_f(d, t, t[v][k])

    return s

def path_large_unjumble(n):
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        d[path_f({}, g).expand()].append(tuple(t))
        # d[path_f({}, g).expand()] += 1
    return d


def path_labeled_r(d, edge_labels, labeling, t, v=0):
    if v in d:
        return d[v]
    elif v > 0 and len(t[v]) == 1:
        return 1
    rpol = 1
    for k in xrange(0 if v == 0 else 1, len(t[v])):
        rpol += sv[labeling[edge_labels[(v, t[v][k])]]] * (path_labeled_r(d, edge_labels, labeling, t, t[v][k]))
    d[v] = rpol
    return d[v]


def path_labeled_f(d, edge_labels, labeling, t, v=0):
    s = path_labeled_r(d, edge_labels, labeling, t, v)
    for i in xrange(0 if v == 0 else 1, len(t[v])):
        for j in xrange(i + 1, len(t[v])):
            xi = sv[labeling[edge_labels[(v, t[v][i])]]]
            xj = sv[labeling[edge_labels[(v, t[v][j])]]]
            s += xi * xj * path_labeled_r(d, edge_labels, labeling, t, t[v][i]) * path_labeled_r(d, edge_labels, labeling, t, t[v][j])

    for k in xrange(0 if v == 0 else 1, len(t[v])):
        s += path_labeled_f(d, edge_labels, labeling, t, t[v][k])

    return s

def path_small_unjumble_labeled(n):
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        # d[path_labeled_f({}, g).expand()] += 1
        for lbl in get_labeled_graphs(t, 2, True):
            d[path_labeled_f({}, edge_lbls, lbl, g).expand()].append((tuple(t), lbl))
            # d[path_labeled_f({}, edge_lbls, lbl, g).expand()] += 1
    return d

def path_small_unjumble_weights(n):
    monomials = [[x**k * y**(i - k) for k in xrange(i + 1)] for i in xrange(1, n)]
    monomials_weights = [[1 * k + 2 * (i - k) for k in xrange(i + 1)] for i in xrange(1, n)]

    # d = defaultdict(int)
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        for lbl in get_labeled_graphs(t, 2, True):
            f = path_labeled_f({}, edge_lbls, lbl, g).expand()

            # wl = [] #[0] * (4 * (n + 1) + 1)
            # for term in str(f).split("+"):
            #     term = term.strip()
            #     if term.find("x") != -1 and term.find("y") != -1:
            #         if term.count("*") > 1:
            #             ii = term.find("*")
            #             term1 = term[: ii]
            #             term2 = term[ii + 1 :].replace("x", "1").replace("y", "2").replace("*", "+").replace("^", "*")
            #             # print term, "t1", eval(term1 + "*(%s)"%term2)
            #             val = eval(term2)
            #             if val >= len(wl):
            #                 wl += [0] * (val - len(wl) + 1)
            #             wl[val] += int(term1)
            #         else:
            #             # print term, "t2", eval(term.replace("x", "1").replace("y", "2").replace("*", "+").replace("^", "*"))
            #             val = eval(term.replace("x", "1").replace("y", "2").replace("*", "+").replace("^", "*"))
            #             if val >= len(wl):
            #                 wl += [0] * (val - len(wl) + 1)
            #             wl[val] += 1
            #     elif not term.isdigit():
            #         # print term, "t3", eval(term.replace("x", "1").replace("y", "2").replace("^", "*"))
            #         ii = term.find("*")
            #         if ii != -1:
            #             term1 = term[: ii]
            #             term2 = term[ii + 1:]
            #             val = eval(term2.replace("x", "1").replace("y", "2").replace("^", "*"))
            #             if val >= len(wl):
            #                 wl += [0] * (val - len(wl) + 1)
            #             wl[val] += int(term1)
            #         else:
            #             val = eval(term.replace("x", "1").replace("y", "2").replace("^", "*"))
            #             if val >= len(wl):
            #                 wl += [0] * (val - len(wl) + 1)
            #             wl[val] += 1

            # print tuple([wl[k] for k in sorted(wl)])
            wl = [0] * (sum(i + 1 for i in lbl) + 1)
            for i in xrange(len(monomials)):
                for j in xrange(i + 2):
                    amonomial = f.coefficient(monomials[i][j])(x=0, y=0)
                    if amonomial != 0:
                        wl[monomials_weights[i][j]] += amonomial

            # print t, lbl, f, wl
            d[tuple(wl)].append((f, t, lbl))
            # d[str(wl)] += 1
    return d


print_statistics(3, 21, path_large_unjumble)
print_statistics(3, 21, path_small_unjumble_labeled)
print_statistics(3, 18, path_small_unjumble_weights)