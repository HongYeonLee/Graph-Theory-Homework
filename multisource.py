# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import math

class op_count(object):
    def __init__(self):
        self.__counter = 0

    def reset(self):
        self.__counter = 0

    def get_counter(self):
        return self.__counter

    def __call__(self, *args, **kwargs):
        self.__counter += 1


class op_add_t(op_count):
    @staticmethod
    def neutral():
        return 0

    def __call__(self, v1, v2):
        super().__call__()
        return v1 + v2


class op_mul_t(op_count):
    @staticmethod
    def neutral():
        return 1

    def __call__(self, v1, v2):
        super().__call__()
        return v1 * v2


class op_and_t(op_count):
    @staticmethod
    def neutral():
        return True

    def __call__(self, v1, v2):
        super().__call__()
        return bool(v1) and bool(v2)


class op_or_t(op_count):
    @staticmethod
    def neutral():
        return False

    def __call__(self, v1, v2):
        super().__call__()
        return bool(v1) or bool(v2)


class op_min_t(op_count):
    @staticmethod
    def neutral():
        return float('inf')

    def __call__(self, v1, v2):
        super().__call__()
        return min(v1, v2)


class op_max_t(op_count):
    @staticmethod
    def neutral():
        return float('-inf')

    def __call__(self, v1, v2):
        super().__call__()
        return max(v1, v2)


op_add = op_add_t()
op_mul = op_mul_t()
op_min = op_min_t()
op_max = op_max_t()
op_and = op_and_t()
op_or = op_or_t()

# Problem 1
#
# Write a function connected_to(n,edges,src) that finds all
# vertices v_j connected to v_src. That is all vertices for which
# there exists a path in the graph starting at v_src and ending
# at v_j.
# Argument n specifies that the graph has n vertices numbered
# from 0 to n-1. Argument edges is a list of pairs of vertices
# denoting undirected edges. If vertex i is adjacent to
# vertex j, then edges contains either the pair (i,j) or
# the pair (j,i).
# Note that the given graphs may not be simple, that is they
# can contain self-loops (edge (i,i)) and multiple edges
# between the same vertices (edge (i,j) and edge (j,i) are
# in edges).
# Note that some of the tests are randomized.
# The function has to return a list containing these vertices
# in any order.


def connected_to(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n
    queue = [src]
    visited[src] = True
    connected_vertices = [src]

    while queue:
        curr = queue.pop(0)
        for neighbor in adj[curr]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
                connected_vertices.append(neighbor)

    return connected_vertices

# Problem 2
#
# In the course the Floyd-Warshall algorithm has been
# presented to you for computing the distance matrix of a
# directed weighted graph. We will denote this matrix M.
# To compute M, the instructions
# M{k,i,j} = min(M{k-1,i,j}, M{k-1,i,k}+M{k-1,k,j})
# are repeated for k from 0 to the number of vertices minus one.
# M{-1,i,j} corresponds to the initialization,
# and we have three cases:
# 1) i==j:
#    M{-1,i,j} = 0
# 2) there exist an edge (i,j,w):
#    M{-1,i,j} = w
# 3) None of the above:
#    M{-1M,i,j} = +inf
#
# This notation can be generalised to:
# M{k,i,j} = M{k-1,i,j} ⊕ (M{k-1,i,k} ⊗ M{k-1,k,j})
# where (M{k,i,j} ∈ H, ⊕, ⊗) is a semiring.
# The operations ⊕ and ⊗ also have neutral elements in H.
# For instance, in the case of H being the integers, the
# neutral element of min (operation ⊕) is +inf, the
# neutral element of + (operation ⊗) is 0.
# Depending on which operations (⊕, ⊗) and neutral elements
# (from the set H) are used, different properties of the graph
# can be computed using Floyd-Warshall.
# In this exercise you are expected to code a generalised
# version of the Floyd-Warshall-algorithm
# floyd_warshall(n,edges, op_plus, e_plus, op_times, e_times)
# which takes the inputs:
# n: number of vertices labeled 0 to n-1
# edges: weighted edges as list of tuples of the form
# [(src_0, dst_0, weight_0), (src_1, dst_1, weight_1), ...]
# op_plus : The operation ⊕
# e_plus : The neutral element of ⊕
# op_times : The operation ⊗
# e_times : The neutral element of ⊗
# Some operations are already predefined, and will be
# passed as arguments to your function by the test cases.
# The operations are given as the functions:
# op_add
# op_min
# op_max
# The algorithm is expected to return the distance matrix
# kM as a list of lists, so that Mij denotes the element
# in the i-th row and j-th column, corresponding to the
# minimal the distance to go from the i-th to the j-th vertex.
# Example how your algorithm will be called:
# M = floyd_warshall_2(n, edges, op_min, math.inf, op_add, 0)
# Remarks
# a) Take care: ⊕/⊗ ("plus"/"times") can denote any of the
#   above defined operations and must not be confused with
#   +/*, the usual addition and multiplication operations
#   over the integers or reals.
# b) It is important to actually implement Floyd-Warshall.
#   The operators used for ⊕ and ⊗ have internal mechanisms
#   that detect repeated calls of Bellmann-Ford for instance.
# c) For the exercises, you can assume that:
#   1) There exists only a single edge between any pair of vertices
#   2) You do not need to implement a detection of negative
#        cycles (or the generalisation thereof), the graphs used
#        for testing do not contain such cycles.
#   3) There are no self-loops (src and dst of an edge are equal)
#
# These exercises were prepared by Philipp Schlehuber-Caissier
# (philipp@lrde.epita.fr).


def floyd_warshall_2(n, edges, op_plus, e_plus, op_times, e_times):
    dist = [[e_plus] * n for _ in range(n)]
    for i in range(n):
        if hasattr(e_times, 'neutral'):
            dist[i][i] = e_times.neutral()
        else:
            dist[i][i] = e_times # 중립 원소 값(int 또는 float)을 직접 사용

    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):
        for i in range(n):
            for j in range(n):
                term2 = op_times(dist[i][k], dist[k][j])
                dist[i][j] = op_plus(dist[i][j], term2)

    return dist


# Problem 3
#
# In the last question you have coded a generalised version of
# the Floyd-Warshall algorithm to take into account different
# operations.
# In this question you will extend its capabilities to not
# only compute the distance matrix, but also the
# "generalised shortest" paths.
# To allow for the computation of the shortest paths, you have
# to use an additional data-structure. This structure holds
# information about the predecessor or successor (depending
# on the implementation) of the vertices and is updated during
# the execution of the algorithm.
# In the course (for the case of ⊕ = min and ⊗ = addition) , this
# was presented as:
# if M{k-1,i,j} > M{k-1,i,k} + M{k-1,k,j}:
#     Update distance matrix
#     Update data-structure
#
# As not all sets are ordered, this notion has to be generalised
# and becomes:
# Compute M{k,i,j}
# if M{k,i,j} != M{k-1,i,j}:
#     Update data-structure
#
# You have to code two functions:
#   A new version of the Floyd-Warshall algorithm that returns
#   not only the distance matrix, but also the data-structure
#   holding the necessary information to compute the path (The
#   inputs remain the same as in the first part).
# A function path(D, source, destination) that outputs the
#   "shortest path" from the vertex source to destination as a
#   function of the data-structure D.
#
# We use the following convention:
# If no path exists from source to destination,
# path(D, source, destination) is expected to return an
# empty list [].
# If source==destination, path is expected to return [source]
# Otherwise, the returned path has to contain all vertices
# visited by the path from source to destination in the correct
# order, including source and destination.
# You can rely on the same assumptions as for the first part
# of the question.
# Example of how your code will be called:
# M,D = floyd_warshall_3(n, edges, op_min, math.inf, op_add, 0)
# Pij = path(D,source,destination)


def floyd_warshall_3(n, edges, op_plus, e_plus, op_times, e_times):
    dist = [[e_plus] * n for _ in range(n)]
    succ = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = e_times.neutral() if hasattr(e_times, 'neutral') else 0
        succ[i][i] = i
    for u, v, w in edges:
        dist[u][v] = w
        succ[u][v] = v

    for k in range(n):
        for i in range(n):
            for j in range(n):
                term1 = dist[i][j]
                term2 = op_times(dist[i][k], dist[k][j])
                new_dist = op_plus(term1, term2)
                if new_dist != dist[i][j]:
                    dist[i][j] = new_dist
                    succ[i][j] = succ[i][k]

    return dist, succ


def path(Succ, source, destination):
    if Succ[source][destination] is None:
        return []
    p = [source]
    while source != destination:
        source = Succ[source][destination]
        p.append(source)
    return p


# Problem 4
#
# In the last part of the question you have implemented a
# generalised version of the Floyd-Warshall algorithm and how
# to use it in order to find the shortest/optimal path in the graph.
# In this question you are asked to implement a specific
# version of the algorithm (i.e. using suitable operations and
# neutral elements) to answer the following question:
# The vertices correspond to cities, the edges correspond to
# the transition from one city to another. The weight on the
# edges (reals taken from the interval [0,1]) corresponds to
# the success rate of the transition. So if the edge
# is (0,1,0.9) you have a 10% chance to die in a horrible
# plane crash when going from city 0 to city 1.
# Your task is to use Floyd-Warshall to compute the safest path
# between two cities called source and destination.
# Code the function:
# safest_path(n,edges,source,destination)
# returning the safest path in the same style as in the last
# question.
# The same assumptions as for the first two parts hold.


def safest_path(n, edges, source, destination):
    def op_max_probability(p1, p2):
        return max(p1, p2)

    class op_mul_probability(op_count):
        @staticmethod
        def neutral():
            return 1.0

        def __call__(self, v1, v2):
            super().__call__()
            return v1 * v2

    op_times_prob = op_mul_probability()
    M, D = floyd_warshall_3(n, edges, op_max_probability, 0.0, op_times_prob, op_times_prob)
    return path(D, source, destination)
