from collections import deque
from functools import partial

from pydstarlite.utility import draw_grid
from pydstarlite.priority_queue import PriorityQueue
from pydstarlite.grid import AgentViewGrid, SquareGrid
from pydstarlite.utility import grid_from_string


class DStarLite(object):
    def __init__(self, graph, start, goal, view_range=2):
        # Init the graphs
        self.graph = AgentViewGrid(graph.width, graph.height)
        self.real_graph: SquareGrid = graph
        self.view_range = view_range

        self.back_pointers = {}
        self.G_VALS = {}
        self.RHS_VALS = {}
        self.Km = 0
        self.position = start
        self.goal = goal
        self.frontier = PriorityQueue()
        self.frontier.put(self.goal, self.calculate_key(self.goal))
        self.back_pointers[self.goal] = None

    def calculate_rhs(self, node):
        lowest_cost_neighbour = self.lowest_cost_neighbour(node)
        self.back_pointers[node] = lowest_cost_neighbour
        return self.lookahead_cost(node, lowest_cost_neighbour)

    def lookahead_cost(self, node, neighbour):
        return self.g(neighbour) + self.graph.cost(neighbour, node)

    def lowest_cost_neighbour(self, node):
        cost = partial(self.lookahead_cost, node)
        return min(self.graph.neighbors(node), key=cost)

    def g(self, node):
        return self.G_VALS.get(node, float('inf'))

    def rhs(self, node):
        return self.RHS_VALS.get(node, float('inf')) if node != self.goal else 0

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def calculate_key(self, node):
        g_rhs = min([self.g(node), self.rhs(node)])

        return (
            g_rhs + self.heuristic(node, self.position) + self.Km,
            g_rhs
        )

    def update_node(self, node):
        if node != self.goal:
            self.RHS_VALS[node] = self.calculate_rhs(node)
        self.frontier.delete(node)
        if self.g(node) != self.rhs(node):
            self.frontier.put(node, self.calculate_key(node))

    def update_nodes(self, nodes):
        [self.update_node(n) for n in nodes]

    def compute_shortest_path(self):
        last_nodes = deque(maxlen=10)
        while self.frontier.first_key() < self.calculate_key(self.position) or self.rhs(self.position) != self.g(self.position):
            k_old = self.frontier.first_key()
            node = self.frontier.pop()
            last_nodes.append(node)
            if len(last_nodes) == 10 and len(set(last_nodes)) < 3:
                raise Exception("Fail! Stuck in a loop")
            k_new = self.calculate_key(node)
            if k_old < k_new:
                self.frontier.put(node, k_new)
            elif self.g(node) > self.rhs(node):
                self.G_VALS[node] = self.rhs(node)
                self.update_nodes(self.graph.neighbors(node))
            else:
                self.G_VALS[node] = float('inf')
                self.update_nodes(self.graph.neighbors(node) + [node])

        return self.back_pointers.copy(), self.G_VALS.copy()

    def move_to_goal(self):
        observation = self.real_graph.observe(self.position, self.view_range)
        walls = self.graph.new_walls(observation)
        self.graph.update_walls(walls)

        self.compute_shortest_path()
        last_node = self.position

        yield self.position, observation, self.graph.walls

        while self.position != self.goal:
            if self.g(self.position) == float('inf'):
                raise Exception("No path")

            self.position = self.lowest_cost_neighbour(self.position)
            observation = self.real_graph.observe(self.position, self.view_range)
            new_walls = self.graph.new_walls(observation)

            if new_walls:
                self.graph.update_walls(new_walls)
                self.Km += self.heuristic(last_node, self.position)
                last_node = self.position
                self.update_nodes({node for wallnode in new_walls
                                   for node in self.graph.neighbors(wallnode)
                                   if node not in self.graph.walls})
                self.compute_shortest_path()
            yield self.position, observation, self.graph.walls



if __name__ == "__main__":
    GRAPH, START, END = grid_from_string("""
    ..........
    ...######.
    .......A#.
    ...######.
    ...#....#.
    ...#....#.
    ........#.
    ........#.
    ........#Z
    ........#.
    """)
    dstar = DStarLite(GRAPH, START, END)
    path = [p for p, o, w in dstar.move_to_goal()]

    print("The graph (A=Start, Z=Goal)")
    draw_grid(GRAPH, width=3, start=START, goal=END)
    print("\n\nPath taken (@ symbols)")
    draw_grid(GRAPH, width=3, path=path)