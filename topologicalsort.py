# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Problem 1
#
# Given a set V = {v0,v1,v2,...,vn-1} and a set of
# constraints {c0, c1, ..., cm} where each constraint is of the
# form (vi, vj).  A topological ordering of V is a permutation of
# V which satisfies all the constraints.   Each constraint (vi,vj)
# has the meaning that vi precedes vj in the ordering.
#
# For example [0,1,3,2] and [0,1,2,3] are both topological
# orderings of {0,1,2,3} subject to constraints [(0,3),(1,2)],
# but [3,1,2,0] is not.  Note also that [1,2,3] and  [1,2,3,2]
# are not permutations of {0,1,2,3} so they are certainly not
# topological orderings thereof.
#
# Write a function is_topological_order(n,constraints,permutation)
# which returns a Boolean indicating whether the given permutation
# is a valid permutation  of  {v0, v1, v2, ..., vn-1} and
# satisfies the given constraints.
# --- n is a positive integer indicating that the sequence is
#     {0, 1, 2, ..., n-1}
# --- constraints is a list of pairs (a,b) indicating that a must
#      precede b
# --- permutation is a list of integers


def is_topological_order(n, constraints, permutation):
    for constraint in constraints:
        for v in constraint:
            assert 0 <= v < n, f"invalid constraint {constraint}"

    if len(permutation) != n or set(permutation) != set(range(n)):
        return False

    pos = {v: i for i, v in enumerate(permutation)}

    for u, v in constraints:
        if pos[u] > pos[v]:
            return False

    return True


# Problem 2
#
# Given a non-empty set V = {0, 1, ..., n-1} and a set of
# constraints {c1, c2, ..., cm} where each constraint is of
# the form (vi, vj)∈V2, a topological ordering of V is a permutation
# of V which satisfies all the constraints.   Each constraint (vi,vj)
# has the meaning that vi precedes vj in the ordering.
# Write a function topological_sort(n,constraints) which returns
# a permutation of [0,1,...,n-1] which satisfies all the constraints.
# If multiple such permutations are possible, return any one of them.
# Be careful!  Sometimes the constraints can be contradictory.
# For example, it is impossible to order {0,1,2} subject to the
# constraints [(0,1),(1,2),(2,0)].
# If no permutation of V exists which satisfies all the
# constraints, the function must return False.


def topological_sort(n, constraints):
    for constraint in constraints:
        for v in constraint:
            assert 0 <= v < n, f"invalid constraint {constraint}"

    graph = [[] for _ in range(n)]
    in_degree = [0] * n

    for u, v in constraints:
        graph[u].append(v)
        in_degree[v] += 1

    queue = [v for v in range(n) if in_degree[v] == 0]
    result = []

    while queue:
        u = queue.pop(0)
        result.append(u)

        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(result) != n:
        return False

    return result
