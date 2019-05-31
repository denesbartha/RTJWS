from collections import defaultdict
from math import log

def successorRooted(L):
    n = len(L)
    p = n - 1
    while L[p] == 1: p = p - 1
    q = p - 1
    if q <= 0: return False
    while L[q] != L[p] - 1: q = q - 1

    s = range(n)
    for i in range(0, p): s[i] = L[i]
    for i in range(p, n): s[i] = s[i - p + q]

    return s


def listLexOrder(L1, L2):
    for i in range(len(L1)):
        if L1[i] < L2[i]:
            return True
        elif L1[i] > L2[i]:
            return False
    return True


def isFree(L):
    n = len(L)
    cnt = 0
    m = 0
    while m < n and cnt < 2:
        if L[m] == 1:
            cnt = cnt + 1
        m = m + 1
    if cnt < 2:
        return False

    L1 = [L[i] - 1 for i in range(1, m - 1)]
    L2 = [L[0]] + [L[i] for i in range(m - 1, n)]
    if max(L2) > max(L1): return True
    if max(L2) < max(L1): return False
    if len(L1) < len(L2): return True
    if len(L1) > len(L2): return False
    return listLexOrder(L1, L2)


def listAllFreeTrees(n):
    L = range(n / 2 + 1) + range(1, (n + 1) / 2)
    while L != False:
        if isFree(L):
            yield L
        L = successorRooted(L)


def gen_tree_edge_list_from_list(L):
    #start node (parent, children list, path list, distance from the root node)
    g = defaultdict(list)
    g[0] = []
    index = 1
    parent = 0
    distance = 0
    edge_lbls = {}
    for i in xrange(1, len(L)):
        if L[i] <= L[i - 1]:
            parent = g[parent][-1]
            distance -= 1
            while distance >= L[i]:
                distance -= 1
                parent = g[parent][0]
        g[index].append(parent)
        g[parent].append(index)

        edge_lbls[(parent, index)] = index - 1
        parent = index
        index += 1
        distance += 1
    return g, edge_lbls


def statistics(n, d):
    mc = 0
    rdtcnt = 0
    class_sizes = defaultdict(lambda: 0)
    for p, lst in d.items():
        ac = len(lst)
        # ac = lst
        if ac > 1:
            # print p, lst
            pass
        if ac > mc:
            mc = ac
        rdtcnt += ac
        class_sizes[ac] += 1

    # https://oeis.org/A000055 Number of trees with n unlabeled nodes.
    # https://oeis.org/A000081 Number of unlabeled rooted trees with n nodes (or connected functions with a fixed point).
    # print "n=%i" % (n)
    # print "number of nonisomorphic rooted directed trees:", rdtcnt
    # print "number of equivalence classes:", len(d)
    # print "ratio:", float(len(d)) / float(rdtcnt)
    # print "maximum sized equivalence class:", mc
    # print "list of class sizes:"
    # sep = "{:%id}" % (len(str(max(class_sizes.values()))))
    # print " ".join([sep.format(i) for i in xrange(min(class_sizes), max(class_sizes) + 1)])
    # print " ".join([sep.format(class_sizes[i]) for i in xrange(min(class_sizes), max(class_sizes) + 1)])
    # print "Entropy: ", -sum(i / float(len(d)) * log(i / float(len(d)), 2) for i in class_sizes.itervalues())
    # print

    print "class_sizes", class_sizes

    ratio = float(len(d)) / float(rdtcnt)
    H1 = log(len(d), 2)
    H2 = -sum(i * s / float(rdtcnt) * log(s / float(rdtcnt), 2) for (s, i) in class_sizes.iteritems())
    entropy =  H1 - H2
    return "\n    ${:,}$ & ${:.0f}$ & ${:.0f}$ & ${ratio}$ & ${:.0f}$ & ${entropy}$ \\\\\n    \\hline".format(n, rdtcnt, len(d), mc, ratio="1" if len(d) == rdtcnt else "{:.6f}".format(ratio), entropy="0" if entropy == 0 else "{:.6f}".format(entropy))


def print_statistics(i, j, fn):
    str = """\\begin{tabularx}{\\textwidth}{| c | c | c | c | c | c |}\n    \\hline\n    \\thead{$\\mathbf{n}$} & \\thead{$\\mathbf{a(n)}$} & \\thead{\\#equivalence \\\\ classes} & \\theadfont{$\\mathbf{\\frac{ec(n)}{a(n)}}$} & \\thead{max. size \\\\ eq. class} & \\thead{entropy} \\\\\n    \\hline"""

    for n in xrange(i, j):
        str += statistics(n, fn(n))
        print n
        print str

    str += """\n\end{tabularx}\n"""
    print
    print
    print str