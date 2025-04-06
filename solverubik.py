# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from lecture.rubik import *
from typing import List, Optional


# initial order        face indices                 face names
#    +--+                 +-----+                    +----+
#    |RR|                 |20 21|                    | U  |
#    |RR|                 |22 23|                    |    |
# +--+--+--+--+     +-----+-----+----+-----+    +----+----+----+----+
# |BB|WW|GG|YY|     |12 13| 0 1 | 4 5| 8  9|    | L  | F  | R  | B  |
# |BB|WW|GG|YY|     |14 15| 2 3 | 6 7|10 11|    |    |    |    |    |
# +--+--+--+--+     +-----+-----+----+-----+    +----+----+----+----+
#    |OO|                 |16 17|                    | D  |
#    |OO|                 |18 19|                    |    |
#    +--+                 +-----+                    +----+
#
# A cube is represented by a string of 24 characters.  Each character is
# the initial of the color of one face, ordered as above.
# However, as an optimization, we use an integer rather than array,
#  i.e. an integer interpreted in base 6, whose kth digit is 0, 1, ...5
#  according to cubeColors (defined below).


from typing import List, Set
from collections import deque


def solve_cube(cube: str, twists: List[str]) -> List[str]:
    initial_state = cubeToInt(cube)
    if solved(initial_state):
        return []

    queue = deque([(initial_state, [])])
    visited: Set[int] = {initial_state}

    while queue:
        current_state, path = queue.popleft()

        for twist_str in twists:
            next_state = rotateCube(current_state, twist_str)

            if next_state not in visited:
                if solved(next_state):
                    return path + [twist_str]
                visited.add(next_state)
                queue.append((next_state, path + [twist_str]))

    return None


if __name__ == '__main__':
    cube, twists = shuffleCube(8, rotations9)
    print(f"{twists=}")
    print(f"{cube=}")
    solution = solve_cube(cube, rotations9)
    print(f"{solution=}")
    c = cubeToInt(cube)
    for twist in solution:
        c = rotateCube(c, twist)
        print(f"{twist} -> {cubeToStr(c)}")
