from pydstarlite.priority_queue import PriorityQueue


class LPAStar(object):
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.back_pointers = {}
        self.G_VALS = {}
        self.RHS_VALS = {}
        self.start = start
        self.goal = goal
        self.frontier = PriorityQueue()
        self.frontier.put(self.start, self.calculate_key(self.start))
        self.back_pointers[self.start] = None

    def calculate_rhs(self, node):
        def lookahead_cost(lowest_cost_neighbour):
            return self.g(lowest_cost_neighbour) + self.graph.cost(lowest_cost_neighbour, node)

        lowest_cost_neighbour = min(self.graph.neighbors(node), key=lookahead_cost)
        self.back_pointers[node] = lowest_cost_neighbour
        return lookahead_cost(lowest_cost_neighbour)

    def g(self, node):
        return self.G_VALS.get(node, float('inf'))

    def rhs(self, node):
        return self.RHS_VALS.get(node, float('inf')) if node != self.start else 0

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def calculate_key(self, node):
        g_rhs = min([self.g(node), self.rhs(node)])

        return (
            g_rhs + self.heuristic(node, self.goal),
            g_rhs
        )

    def update_node(self, node):
        if node != self.start:
            self.RHS_VALS[node] = self.calculate_rhs(node)
        self.frontier.delete(node)
        if self.g(node) != self.rhs(node):
            self.frontier.put(node, self.calculate_key(node))

    def update_nodes(self, nodes):
        [self.update_node(n) for n in nodes]

    def compute_shorted_path(self, incremental=False):

        while self.frontier.first_key() < self.calculate_key(self.goal) or self.rhs(self.goal) != self.g(self.goal):
            node = self.frontier.pop()

            if self.g(node) > self.rhs(node):
                self.G_VALS[node] = self.rhs(node)
                self.update_nodes(self.graph.neighbors(node))
            else:
                self.G_VALS[node] = float('inf')
                self.update_nodes(self.graph.neighbors(node) + [node])

            if incremental:
                yield self.G_VALS

        return self.back_pointers.copy(), self.G_VALS.copy()