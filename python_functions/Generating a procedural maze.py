import random
from collections import deque

def generate_maze(width, height):
    maze = [["#"] * (width * 2 + 1) for _ in range(height * 2 + 1)]

    def break_wall(x, y, dx, dy):
        maze[y * 2 + dy][x * 2 + dx] = ' '
        stack.append((x + dx, y + dy))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    stack = deque([(0, 0)])
    maze[1][1] = ' '

    while stack:
        x, y = stack[-1]
        available_directions = [
            (dx, dy) for dx, dy in directions
            if 0 <= x + dx * 2 < width and
            0 <= y + dy * 2 < height and
            maze[(y * 2) + (dy * 2) + dy][(x * 2) + (dx * 2) + dx] == "#"
        ]

        if not available_directions:
            stack.pop()
            continue

        dx, dy = random.choice(available_directions)
        break_wall(x, y, dx, dy)

    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(row))

if __name__ == "__main__":
    maze = generate_maze(20, 10)
    print_maze(maze)