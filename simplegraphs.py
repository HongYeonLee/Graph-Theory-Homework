# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Problem 1
#
# Write a function odd_vertices(n, edges) that returns
# the list of odd-degree vertices sorted in ascending order.
# The degree of a vertex is the number of edges incident
# to that vertex.
# Argument n specifies that the graph has n>0 vertices
# numbered from 0 to n-1. Argument edges is a list of pairs of
# vertices denoting undirected edges. If vertex i is connected
# to vertex j, then edges contains either the pair (i,j) or
# the pair (j,i). If a vertex does not appear in any edge, it is
# an isolated vertex and thus has degree 0 (which is even).
# If a pair appears multiple times in edges (in either order),
# this means the corresponding vertices are linked multiple times.
# A loop of the form (i,i) contributes 2 to the degree of vertex i.
def odd_vertices(n, edges):
    # 인접 행렬 초기화
    adj_matrix = [[0] * n for _ in range(n)]

    # 간선 정보를 인접 행렬에 반영
    for u, v in edges:
        adj_matrix[u][v] += 1
        adj_matrix[v][u] += 1

    # 차수가 홀수인 정점 찾기
    result = []
    for i in range(n):
        degree = sum(adj_matrix[i])
        if degree % 2 == 1:
            result.append(i)

    return result

# Problem 2
#
# Write a function is_simple(n, edges) that decides whether
# an undirected graph is simple.
# Argument n specifies that the graph has n>0 vertices numbered
# from 0 to n-1. Argument edges is a list of pairs of vertices
# denoting undirected edges. If vertex i is connected to
# vertex j, then edges contains either the pair (i,j) or
# the pair (j,i). If a pair appears multiple times in edges
# (in any order), this means the corresponding vertices are linked
# multiple times.
# A graph is simple if no two vertices are connected more than
# once, and the graph has no loop of the form (i,i).
# The function should return True if the graph is simple, and
# False otherwise.
def is_simple(n, edges):
    # 인접 행렬 초기화
    adj_matrix = [[0] * n for _ in range(n)]

    # 간선 정보를 인접 행렬에 반영
    for u, v in edges:
        # 루프가 존재하면 simple하지 않음
        if u == v:
            return False

        # 중복된 간선이 존재하면 simple하지 않음
        if adj_matrix[u][v] > 0:
            return False

        adj_matrix[u][v] += 1
        adj_matrix[v][u] += 1

    return True


# Problem 3
#
# Write a function is_connected(n,edges) that decides
# whether an undirected graph is connected (i.e. there exists
# a path between any two vertices).
# Argument n specifies that the graph has n>0 vertices numbered
# from 0 to n-1. Argument edges is a list of pairs of vertices
# denoting undirected edges (if vertex i is connected to
# vertex j, then edges contains either the pair (i,j) or the
# pair (j,i)).
# The function should return True if the graph is connected,
# or False otherwise.
def is_connected(n, edges):
    assert n > 0

    # Step 1: Build the adjacency list
    adj_list = {i: [] for i in range(n)}

    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)  # Since the graph is undirected

    # Step 2: DFS function to explore the graph
    def dfs(vertex, visited):
        visited.add(vertex)
        for neighbor in adj_list[vertex]:
            if neighbor not in visited:
                dfs(neighbor, visited)

    # Step 3: Start DFS from vertex 0
    visited = set()
    dfs(0, visited)

    # Step 4: Check if all vertices were visited
    return len(visited) == n


# Problem 4
#
# Write a function is_edge_connected(n,edge) that decides
# whether an undirected graph is edge-connected (i.e. any two
# edges can be part of a common path).
# Argument n specifies that the graph has n>0 vertices numbered
# from 0 to n-1. Argument edges is a list of pairs of vertices
# denoting undirected edges (if vertex i is connected to
# vertex j, then edges contains either the pair (i,j) or the
# pair (j,i)).
# The function should return True if the graph is edge-connected,
# or False otherwise.
def is_edge_connected(n, edges):
    assert n > 0
    for e in edges:
        assert type(e) is tuple

    # Step 1: Build the adjacency list
    adj_list = {i: [] for i in range(n)}
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)

    # Step 2: Variables for DFS and bridge finding
    disc = [-1] * n  # Discovery times of visited vertices
    low = [-1] * n  # Lowest points reachable
    parent = [-1] * n
    time = [0]  # Mutable time counter
    bridges = []  # To store the bridges

    # Step 3: DFS to find bridges
    def dfs(u):
        disc[u] = low[u] = time[0]
        time[0] += 1

        for v in adj_list[u]:
            if disc[v] == -1:  # If v is not visited
                parent[v] = u
                dfs(v)

                # Check if the subtree rooted at v has a connection back to one of u's ancestors
                low[u] = min(low[u], low[v])

                # If the lowest vertex reachable from v is below u, then (u, v) is a bridge
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent[u]:  # Back edge to an already visited vertex
                low[u] = min(low[u], disc[v])

    # Step 4: Call DFS for each unvisited vertex
    for i in range(n):
        if disc[i] == -1:
            dfs(i)

    # Step 5: If any bridges were found, return False (graph is not edge-connected)
    return len(bridges) == 0