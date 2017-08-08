class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def cost(self, from_node, to_node):
        return 1

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        SquareGrid.__init__(self, width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


def grid_from_string(string):
    lines = [l.strip() for l in string.split('\n') if l.strip()]
    grid = SquareGrid(len(lines[0]), len(lines))
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                grid.walls.append((col, row))
    return grid