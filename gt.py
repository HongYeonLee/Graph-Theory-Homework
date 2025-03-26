# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Problem 1
#
# Write a function eccentricity(n,edge,i) that compute the
# eccentricity of vertex i.
# Argument n specifies that the directed graph has n>0 vertices
# numbered from 0 to n-1. Argument edges is a list of pairs of
# vertices denoting directed edges. If vertex i has an outgoing
# edge going to vertex j, then edges contains the pair (i,j).
# The distance dist(i,j) between two vertices i and j is the
# minimum number of edges of paths that connect i to j. If i=j,
# their distance is 0. The eccentricity of vertex i is the maximum
# distance dist(i,j) to all other vertices j. If the graph is
# not connected, the eccentricity of all vertices is math.inf.
import math


def eccentricity(n, edges, i):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    max_dist = 0
    for j in range(n):
        if i == j:
            continue
        dist = distance(n, edges, i, j, adj)
        if dist == math.inf:
            return math.inf
        max_dist = max(max_dist, dist)

    return max_dist


# Problem 2
#
# Write a function distance(n,edge,i,j) that compute the
# distance between vertices i and j.
# Argument n specifies that the graph has n>0 vertices numbered
# from 0 to n-1. Argument edges is a list of pairs of vertices
# denoting undirected edges. If vertex i is connected to vertex j,
# then edge contains either the pair (i,j) or the pair (j,i).
# If a pair appears multiple time in edge (in any order), it means
# the corresponding vertices are linked multiple times.
# The distance between two vertices i and j is the minimum number
# of edges of paths that connect i to j. If i=j, their distance
# is 0, and if the two vertices are not connected, their distance
# should be returned as math.inf.


def distance(n, edges, i, j, adj=None):
    if i == j:
        return 0

    if adj is None:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

    queue = [(i, 0)]
    visited = {i}

    while queue:
        curr, dist = queue.pop(0)
        if curr == j:
            return dist

        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return math.inf
