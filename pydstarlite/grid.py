WALL = '#'
PASSABLE = '.'

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = set()

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def cost(self, from_node, to_node):
        if from_node in self.walls or to_node in self.walls:
            return float('inf')
        else:
            return 1

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        return list(results)

    def observe(self, position, obs_range=2):
        (px, py) = position
        nodes = [(x, y) for x in range(px - obs_range, px + obs_range + 1)
                        for y in range(py - obs_range, py + obs_range + 1)
                 if self.in_bounds((x, y))]
        return {node: WALL if node in self.walls else PASSABLE for node in nodes}


class AgentViewGrid(SquareGrid):

    def new_walls(self, observation):
        walls_in_obs = {node for node, nodetype in observation.items()
                        if nodetype == WALL}
        return walls_in_obs - self.walls

    def update_walls(self, new_walls):
        self.walls.update(new_walls)

