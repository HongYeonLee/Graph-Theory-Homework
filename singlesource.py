# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import math
from typing import List, Tuple, Optional
import heapq

# Problem 1
#
# Measuring a path in a directed weighted graph
# In this exercise you will be given a simple graph as a list
# of directed, weighted, edges and a list of vertices.  You will
# determine the length of the path designated by the vertices.
#
# You must write a function find_path_distance(n,edges,path).
# n indicates the number of vertices in the graph
# edges is a list of triples (a,b,w) indicating that the edge
# from a to b has weight w
# path a list of vertices which may or may not designate a path
# in the graph.
# If path does not designate a valid path, then find_path_distance
# should return None. Otherwise, find_path_distance should return
# the distance from path[0] to path[len(path)-1] along the path.
# A path is invalid if it is an empty list, if it contains a
# non-vertex, or if it contains two adjacent elements which do
# not designate an edge. E.g., if the edges are {(1,2),(2,3),(2,4)},
# then [1,2,4] is a valid path, but [3,2,4] is not.


def find_path_distance(n, edges, path):
    if not path:
        return None

    for vertex in path:
        if not (0 <= vertex < n):
            return None

    adj = {}
    for u, v, w in edges:
        if u not in adj:
            adj[u] = []
        adj[u].append((v, w))

    total_distance = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        found_edge = False
        if u in adj:
            for neighbor, weight in adj[u]:
                if neighbor == v:
                    total_distance += weight
                    found_edge = True
                    break
        if not found_edge:
            return None

    return total_distance
# Problem 2
#
# Single source shortest paths on weighted, UNDIRECTED graph
#
# You will be given a list of triples [(a,b,w),...] representing
# weighted edges of an undirected graph.
# In this exercise we are only interested in connected graphs.
# There will be no test cases containing disconnected graphs.
# You may also assume that for any two vertices a and b, there is
# at most one edge between a and b.
# In this exercise (a,b) represents an undirected edge, meaning
# the distance from a to b is w, and also the distance from b to a
# is w.
# You must write a function single_source_distances_undirected(n,edges,src)
# which takes the parameters
# --- n, the number of vertices.  The vertices are numbered
#        from 0 to n-1,
# --- edges, a list of triples indicating undirected weighted edges.
#        Each triple of the form (a,b,w) as described above,
# --- src, the starting vertex.
#
# Your function should return None if the graph has a negative
# weight cycle, otherwise it should return a list dist such that
# dist[v] is the distance of the shortest path from src to v.


def single_source_distances_undirected(n, edges, src):
    dist = [math.inf] * n
    dist[src] = 0

    directed_edges = []
    for u, v, w in edges:
        directed_edges.append((u, v, w))
        directed_edges.append((v, u, w))

    for _ in range(n - 1):
        updated = False
        for u, v, w in directed_edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    for u, v, w in directed_edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            return None

    return dist


# Problem 3
#
# Single source shortest paths on weighted, DIRECTED graph
#
# You will be given a list of triples [(a,b,w),...] representing
# weighted, directed edges.
# In this exercise the graphs are not necessarily strongly connected.
# In this exercise (a,b) represents a directed edge, meaning
# the distance from a to b is w, but careful, it does not mean the
# distance from b to a is w.  However, there is at most one edge
# from a to b and at most one edge from b to a.
# You must write a function single_source_distances_directed(n,edges,src)
# which takes the parameters
# --- n, the number of vertices.  The vertices are numbered
#          from 0 to n-1,
# --- edges, a list of triples indicating directed weighted edges.
#          Each triple of the form (a,b,w) as described above,
# --- src, the starting vertex.
#
# Your function should return None if the graph has a negative
# weight cycle, otherwise it should return a list dist such
# that dist[v] is the distance of the shortest path from
# src to v. If vertex v is not reachable from the given src
# vertex, then dist[v] should be math.inf.


def single_source_distances_directed(n, edges, src):
    dist = [math.inf] * n
    dist[src] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            return None

    return dist


# Problem 4
#
# Find a shortest path in a directed, weighted graph
#
# In this exercise you are not asked the distance, but rather
# the actual path which minimizes the distance between two vertices
# in a given directed, weighted graph.
# You will be given an array of triples (a,b,w) representing
# weighted edges.
# In this exercise we work on graphs that may not be strongly
# connected.
# In this exercise (a,b) represents a directed edge, meaning
# the distance from a to b is w, but careful, it does not mean
# the distance from b to a is w. However, there is at most one
# edge from a to b and at most one edge from b to a.
# You must write a function shortest_path(n,edges,src,dst)
# which takes the parameters
# --- n, the number of vertices.  The vertices are numbered from
#          0 to n-1,
# --- edges, a list of triples indicating directed weighted edges.
#          Each triple of the form (a,b,w) as described above,
# --- src, the starting vertex,
# --- dst, the destination vertex.
#
# Your function should return None if the graph has a negative
# weight cycle, or if there is no path from src to dst,
# otherwise it should return a list of vertices indicating
# the shortest path from src to dst.  So the first element of
# the returned list must be src, and the final element
# should be dst.


def shortest_path(n, edges, src, dst):
    dist = [math.inf] * n
    dist[src] = 0
    parent = [-1] * n

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break

    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            return None  # Negative weight cycle

    if dist[dst] == math.inf:
        return None  # No path

    path = []
    curr = dst
    while curr != -1:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]
