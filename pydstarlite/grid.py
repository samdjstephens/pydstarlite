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



class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        SquareGrid.__init__(self, width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


def grid_from_string(string):
    lines = [l.strip() for l in string.split('\n') if l.strip()]
    grid = SquareGrid(len(lines[0]), len(lines))
    start, end = None, None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == WALL:
                grid.walls.add((col, row))
            if char == 'A':
                start = (col, row)
            if char == 'Z':
                end = (col, row)
    assert start is not None
    assert end is not None
    return grid, start, end