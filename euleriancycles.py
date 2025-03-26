from typing import Any, List, Tuple, Optional, Set

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Problem 1
#
# Write a function is_eulerian(n,edge) that decides if a graph
# is Eulerian.
# Argument n specifies that the graph has n vertices numbered
# from 0 to n-1. Argument edges is a list of pairs of vertices
# denoting undirected edges. If vertex i is connected to
# vertex j, then edge contains either the pair (i,j) or
# the pair (j,i). If a pair appears multiple times in edge
# (in any order), it means the corresponding vertices are
# linked multiple times.
# Edges of the form (i,i) ARE ALLOWED.
# The function should return True if the graph contains
# an Eulerian cycle (i.e., a cycle that visits each edge
# exactly once), and False otherwise. Note that a graph with
# no edge is Eulerian (an empty cycle will visit all edges).


def is_eulerian(n, edges):
    if not edges:
        return True

    adj = [[] for _ in range(n)]
    degree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    count = 0
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs(v)

    for i in range(n):
        if degree[i] > 0:
            dfs(i)
            break

    for i in range(n):
        if degree[i] > 0 and not visited[i]:
            return False

    odd_degree_count = 0
    for d in degree:
        if d % 2 != 0:
            odd_degree_count += 1

    return odd_degree_count == 0


# Problem 2
#
# Write a function find_eulerian_cycle(m,edges) that finds an
# Eulerian cycle in a graph if the graph is Eulerian.
#
# If there is no Eurlerian cycle, the function should return None.
#
# Argument m specifies that the graph has m vertices numbered
# from 0 to m-1. Argument edges is a list of pairs of vertices
# denoting undirected edges. If vertex i is connected to
# vertex j, then edges contains either the pair (i,j) or
# the pair (j,i). If a pair appears multiple times in edges
# (in any order), it means the corresponding vertices are
# linked multiple times.
# Edges of the form (i,i) ARE ALLOWED.
# Let's assume len(edges)=n.
# The function should return a list of vertex numbers
# [v0,v1,v2,...,vn-1] such that the n edges
# (v0,v1),(v1,v2),(v2,v3),...,(vn-2,vn-1),(vn-1,v0)
# form a cycle that visits each edge of the graph exactly once.
# For clarification, if there are n edges, then this function
# must return a list of length=n or None.
# The list might have repeated vertices.
# E.g, if len(edges)=12, then return a list of length 12,
# or else return None if no such cycle exists.
from collections import defaultdict


def find_eulerian_cycle(m, edges):
    if not is_eulerian(m, edges):
        return []

    adj = [[] for _ in range(m)]
    edge_counts = {}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        edge_counts[(min(u, v), max(u, v))] = edge_counts.get((min(u, v), max(u, v)), 0) + 1

    stack = [0]
    cycle = []
    while stack:
        u = stack[-1]
        if adj[u]:
            v = adj[u].pop()
            adj[v].remove(u)
            edge_key = (min(u, v), max(u, v))
            edge_counts[edge_key] -= 1
            if edge_counts[edge_key] == 0:
                del edge_counts[edge_key]
            stack.append(v)
        else:
            cycle.append(stack.pop())

    if len(cycle) - 1 != len(edges):
        return []

    result = []
    for i in range(len(cycle) - 1):
        result.append(cycle[i])

    return result[::-1]


# Problem 3
#
# Write a function is_eulerian_cycle(n,edge,cycle) that decides
# if a cycle is Eulerian, i.e., it visits each edge of the given
# graph exactly once.
#
# Argument n specifies that the graph has m vertices numbered
# from 0 to n-1. Argument edges is a list of pairs of vertices
# denoting undirected edges. If vertex i is connected to
# vertex j, then edge contains either the pair (i,j) or
# the pair (j,i). If a pair appears multiple time in edge
# (in any order), it means the corresponding vertices are
# linked multiple times.
# Edges of the form (i,i) ARE ALLOWED.
#
# Argument cycle is a list of m>=0 vertex numbers
# [v0,v1,v2,...,vm-1], a list of length=m, denoting a cycle consisting of m edges
# (v0,v1),(v1,v2),(v2,v3),...,(vm-2,vm-1),(vm-1,v0).
# Note that if the input graph contains multiple occurrences of
# some edge (i,j), then an Eulerian cycle must have as many
# occurrences of this edge.
#
# The function should return True if the given cycle is
# Eulerian and False otherwise.
#
# For clarification, an Eulerian cycle is a length of length = len(edges)
# consisting of vertices, each 0 <= v < n, possibly having some vertices
# repeating, and possibly omitting some vertices.


def is_eulerian_cycle(n, edges, cycle):
    if not edges:
        return len(cycle) == 1 and cycle[0] == 0

    if not cycle:
        return False

    edge_counts = {}
    for u, v in edges:
        edge_counts[(min(u, v), max(u, v))] = edge_counts.get((min(u, v), max(u, v)), 0) + 1

    cycle_edge_counts = {}
    for i in range(len(cycle) - 1):
        u, v = cycle[i], cycle[i + 1]
        cycle_edge_counts[(min(u, v), max(u, v))] = cycle_edge_counts.get((min(u, v), max(u, v)), 0) + 1
    u, v = cycle[-1], cycle[0]
    cycle_edge_counts[(min(u, v), max(u, v))] = cycle_edge_counts.get((min(u, v), max(u, v)), 0) + 1

    if len(edges) != len(cycle):
        return False

    return edge_counts == cycle_edge_counts
