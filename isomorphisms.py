# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Write a function is_isomorphism(n, edges2, edges2, bij) that
# decides whether the two given graphs are isomorphic and
# in particular whether the given bij is the bijection.
# Argument n specifies that the graph1 and graph2 both have
# n vertices, numbered from 0 to n-1. Arguments edges1 and edges2
# are each a list of pairs of vertices denoting undirected edges.
# If vertex i is connected to vertex j, then the edge contains
# either the pair (i,j) or the pair (j,i). A pair never appears
# multiple times in the same list.  And if (i,j) appears in
# one edge list then (j,i) does not appear in the same edge list.
# The semantics of bij are as follows:  bij is a list of length n.
# If bij[j] = k, this means that vertex j of graph1 corresponds
# to vertex k in graph2.  If bij is in fact a bijection, this
# also means that vertex k in graph2 corresponds to vertex j
# in graph1.
# Note that if bij is not really a bijection, then your function
# should return False.
# Your function should return True or False if the given bij is
# an isomorphism from graph1 to graph2.


def is_isomorphism(n, edges1, edges2, bij):
    if len(bij) != n or len(set(bij)) != n:
        return False

    if len(edges1) != len(edges2):
        return False

    for b in bij:
        if b >= n:
            return False

    for u, v in edges1:
        u_mapped = bij[u]
        v_mapped = bij[v]
        if (u_mapped, v_mapped) not in edges2 and (v_mapped, u_mapped) not in edges2:
            return False

    return True
