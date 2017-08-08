# Sample code from http://www.redblobgames.com/pathfinding/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>


# utility functions for dealing with square grids
from pydstarlite.grid import GridWithWeights, SquareGrid, grid_from_string
from pydstarlite.queue import PriorityQueue


def from_id_width(id, width):
    return id % width, id // width


def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][
        id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = "\u2192"
        if x2 == x1 - 1: r = "\u2190"
        if y2 == y1 + 1: r = "\u2193"
        if y2 == y1 - 1: r = "\u2191"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if id in graph.walls: r = "#" * width
    return r


def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width),
                  end="")
        print()

# data from main article
DIAGRAM1_WALLS = [from_id_width(id, width=30) for id in
                  [21, 22, 51, 52, 81, 82, 93, 94, 111, 112, 123, 124, 133,
                   134, 141, 142, 153, 154, 163, 164, 171, 172, 173, 174,
                   175, 183, 184, 193, 194, 201, 202, 203, 204, 205, 213,
                   214, 223, 224, 243, 244, 253, 254, 273, 274, 283, 284,
                   303, 304, 313, 314, 333, 334, 343, 344, 373, 374, 403,
                   404, 433, 434]]

diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagram4.weights = {loc: 1 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}


diagram5 = grid_from_string("""
..........
..........
..........
...######.
...#......
...#......
...#......
.###......
.###......
..........
""")


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.pop()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far



def lpa_star_search(graph, start, goal):
    G_VALS = {}
    RHS_VALS = {}

    def calculate_rhs(node):
        def lookahead_cost(lowest_cost_neighbour):
            return g(lowest_cost_neighbour) + graph.cost(lowest_cost_neighbour, node)

        lowest_cost_neighbour = min(graph.neighbors(node), key=lookahead_cost)
        back_pointers[node] = lowest_cost_neighbour
        return lookahead_cost(lowest_cost_neighbour)

    def rhs(node):
        return RHS_VALS.get(node, float('inf')) if node != start else 0

    def g(node):
        return G_VALS.get(node, float('inf'))

    def calculate_key(node):
        g_rhs = min([g(node), rhs(node)])

        return (
            g_rhs + heuristic(node, goal),
            g_rhs
        )

    def update_node(node):
        if node != start:
            RHS_VALS[node] = calculate_rhs(node)
        frontier.delete(node)
        if g(node) != rhs(node):
            frontier.put(node, calculate_key(node))

    def update_nodes(nodes):
        [update_node(n) for n in nodes]

    frontier = PriorityQueue()
    back_pointers = {}

    # Initialise
    frontier.put(start, calculate_key(start))
    back_pointers[start] = None

    while frontier.first_key() < calculate_key(goal) or rhs(goal) != g(goal):
        node = frontier.pop()

        if g(node) > rhs(node):
            G_VALS[node] = rhs(node)
            update_nodes(graph.neighbors(node))
        else:
            G_VALS[node] = float('inf')
            update_nodes(graph.neighbors(node) + [node])

    return back_pointers.copy(), G_VALS.copy()
