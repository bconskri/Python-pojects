class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        self.adaptee.set_dim((len(grid[0]),len(grid)))

        lights = []
        obstacles = []
        for i, row in enumerate(grid):
            for j, elem in enumerate(row):
                if elem == 1:
                    lights += [(j, i)]
                if elem == -1:
                    obstacles += [(j, i)]

        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)

        return self.adaptee.generate_lights()