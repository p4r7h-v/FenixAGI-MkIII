import numpy as np

def game_of_life(grid, generations):
    def count_neighbors(x, y, grid):
        count = 0
        rows, cols = len(grid), len(grid[0])

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not (i == x and j == y) and 0 <= i < rows and 0 <= j < cols:
                    count += grid[i][j]
        return count

    def evolve(grid):
        new_grid = np.zeros_like(grid)
        rows, cols = len(grid), len(grid[0])

        for i in range(rows):
            for j in range(cols):
                neighbors = count_neighbors(i, j, grid)
                if grid[i][j] and neighbors in {2, 3}:
                    new_grid[i][j] = 1
                elif not grid[i][j] and neighbors == 3:
                    new_grid[i][j] = 1
        return new_grid

    for _ in range(generations):
        grid = evolve(grid)

    return grid