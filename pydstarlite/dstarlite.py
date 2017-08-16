from pydstarlite.priority_queue import PriorityQueue
from pydstarlite.grid import AgentViewGrid, SquareGrid


class DStarLite(object):
    def __init__(self, graph, start, goal):
        # Init the graphs
        self.graph = AgentViewGrid(graph.width, graph.height)
        self.real_graph: SquareGrid = graph

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
        def lookahead_cost(neighbour):
            return self.g(neighbour) + self.graph.cost(neighbour, node)

        lowest_cost_neighbour = min(self.graph.neighbors(node), key=lookahead_cost)
        self.back_pointers[node] = lowest_cost_neighbour
        return lookahead_cost(lowest_cost_neighbour)

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

        while self.frontier.first_key() < self.calculate_key(self.position) or self.rhs(self.position) != self.g(self.position):
            k_old = self.frontier.first_key()
            node = self.frontier.pop()
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
        observation = self.real_graph.observe(self.position)
        walls = self.graph.new_walls(observation)
        self.graph.update_walls(walls)

        self.compute_shortest_path()
        last_node = self.position

        yield self.position, observation, self.graph.walls

        while self.position != self.goal:
            if self.g(self.position) == float('inf'):
                raise Exception("No path")

            self.position = self.lowest_cost_neighbour(self.position)
            observation = self.real_graph.observe(self.position)
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


    def lowest_cost_neighbour(self, node):
        """TODO: Refactor above to use this"""
        def lookahead_cost(neighbour):
            return self.g(neighbour) + self.graph.cost(neighbour, node)

        return min(self.graph.neighbors(node), key=lookahead_cost)