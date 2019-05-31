from copy import copy
from collections import defaultdict
from tree_labeling import get_labeled_graphs
from list_free_trees import listAllFreeTrees, gen_tree_edge_list_from_list, print_statistics
# from sage.all import *
#
# # turn off the warnings (because of sage)...
# warnings.filterwarnings('ignore')
#
# # introduce a new symbolic variable
# x = sage.all.SR.var('x')

def try_place(S, weights, maxpaths, X, width, y):
    S2 = S[::]
    for i in xrange(len(X)):
        a = abs(X[i] - y)
        if a not in S2:
            return False
        S2.remove(a)
    X.append(y)
    if not place(S2, weights, maxpaths, X, width):
        del X[-1]
        return False
    return True


def place(S, weights, maxpaths, X, width):
    # if we have created a possible path
    if len(X) == len(maxpaths[0]):
        path = maxpaths[0]
        X2 = sorted(X)

        #create a copy of the weigths dict and place the new-found elements on the edges
        weights2 = copy(weights)
        for i in xrange(len(path) - 1):
            (u, v) = weight_pair(path[i], path[i + 1])
            # if the edge hasn't got any element
            if weights2[(u, v)] == None:
                # the edge's label will be the difference of the two actual neighbours on the path
                weights2[(u, v)] = X2[i + 1] - X2[i]
            # otherwise the actual edge has to be the same as the difference of the two actual neighbours
            elif weights2[(u, v)] != X2[i + 1] - X2[i]:
                return False
        return find_weights(S, weights2, maxpaths[1 : ])

    # this contains the possible distances: for every s in S: {s, width - s} in possible_dist_set
    possible_dist_set = set(S)
    for s in S:
        possible_dist_set.add(width - s)
    for actual_dist in possible_dist_set:
        if try_place(S, weights, maxpaths, X, width, actual_dist):
            return True

    return False


def find_weights(S, weights, maxpaths):
    if maxpaths == []:
        # if there is no more path remained and if S is empty => we are done
        if S == []:
            print weights
            return True
        return False
    # the actual path
    path = maxpaths[0]
    n = len(path)
    direction = []
    # if the first edge is known
    if weights[weight_pair(path[0], path[1])] != None:
        direction = xrange(n - 1)
    # if the last edge is known
    elif weights[weight_pair(path[-2], path[-1])] != None:
        direction = xrange(n - 2, -1, -1)
    X = [0]
    dist = 0
    # recover distances from the weights
    for i in direction:
        w = weights[weight_pair(path[i], path[i + 1])]
        if w == None:
            break
        dist += w
        X.append(dist)

    if X[-1] > S[-1]:
        return False

    # this set will contain the distances that we try out
    Tried = set([])
    for i in xrange(len(S) - 1, -1, -1):
        width = S[i]
        # if the actual width is not in the set => try it out
        if width not in Tried:
            Tried.add(width)

            # copy the multiset except the actual element
            S2 = S[ : i] + S[i + 1 : ]
            if S2 != []:
                if len(X) > 2:
                    # remove the distances from the beginning of the path
                    for i in xrange(1, len(X)):
                        if width - X[i] not in S2:
                            return False
                        S2.remove(width - X[i])
                if place(S2, weights, copy(maxpaths), X + [width], width):
                    return True
            # if S has only one element which is the same as the last element of the path
            elif width == X[-1]:
                if place([], weights, copy(maxpaths), X, width):
                    return True
    return False


def find_maximal_paths_from_node(graph, start, parent, node, maxpaths, actualpath = []):
    actualpath.append(node)
    #if we are at a leaf
    if len(graph[node]) <= 1 and node != start:
        for mp in maxpaths:
            # if the actual path is already in the maxpaths vector => it is not a new path
            if mp[-1] == start and mp[0] == node:
                break
        else:
            maxpaths.append(actualpath[::])
    else:
        for u in graph[node]:
            if parent == None or u != parent:
                find_maximal_paths_from_node(graph, start, node, u, maxpaths, actualpath)
    del actualpath[-1]


def find_maximal_paths(graph):
    maxpaths = []
    #for every leaf
    for u in graph:
        if len(graph[u]) == 1:
            find_maximal_paths_from_node(graph, u, None, u, maxpaths)
    maxpaths.sort(key = lambda mp: len(mp))
    return maxpaths


def max_path_large_unjumble(n):
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        d[tuple([len(p) for p in find_maximal_paths(g)])].append(tuple(t))
    return d


def max_path_small_unjumble(n):
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        # print t
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        mp = find_maximal_paths(g)
        # print mp
        for lbl in get_labeled_graphs(t, 2, True):
            coloring = []
            for mpindex in xrange(len(mp)):
                p = mp[mpindex]
                colorcnt = [0, 0]
                for i in xrange(1, len(p)):
                    x, y = min(p[i], p[i - 1]), max(p[i], p[i - 1])
                    colorcnt[lbl[edge_lbls[(x, y)]]] += 1
                # print "".join(map(str, get_smaller_color(acoloring))), lbl
                coloring.append(tuple(colorcnt))
            d[tuple(sorted(coloring))].append((tuple(t), lbl))
            # d[tuple(sorted(coloring))] += 1
            # print lbl, str(coloring)
    # print d
    return d


def max_path_small_unjumble_with_weighted(n, weights=(1, 2)):
    d = defaultdict(list)
    for t in listAllFreeTrees(n):
        # print t
        g, edge_lbls = gen_tree_edge_list_from_list(t)
        mp = find_maximal_paths(g)
        # print mp
        for lbl in get_labeled_graphs(t, 2, True):
            coloring = []
            # sc = []
            for mpindex in xrange(len(mp)):
                p = mp[mpindex]
                w = 0
                for i in xrange(1, len(p)):
                    x, y = min(p[i], p[i - 1]), max(p[i], p[i - 1])
                    w += weights[lbl[edge_lbls[(x, y)]]]
                # if mpindex > 0 and len(mp[mpindex]) > len(mp[mpindex - 1]):
                #     coloring += sorted(sc)
                #     coloring.append("|")
                #     sc = []
                # sc.append(str(w))
                coloring.append(w)
            # coloring += sorted(sc)
            # print lbl, str(coloring)
            # d[tuple(sorted(coloring))] += 1
            d[tuple(sorted(coloring))].append((tuple(t), lbl))
            # d[tuple(sorted(coloring))] += 1
    return d


# print_statistics(3, 21, max_path_large_unjumble)
print_statistics(3, 16, max_path_small_unjumble)
# print_statistics(3, 16, max_path_small_unjumble_with_weighted)
