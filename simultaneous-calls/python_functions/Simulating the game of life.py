import numpy as np

def game_of_life(board, iterations):
    def get_neighbors(x, y, board):
        neighbors = []
        for i in range(max(0, x - 1), min(board.shape[0], x + 2)):
            for j in range(max(0, y - 1), min(board.shape[1], y + 2)):
                if (i, j) != (x, y):
                    neighbors.append(board[i, j])
        return neighbors

    def next_generation(board):
        new_board = np.zeros_like(board)
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                alive_neighbors = sum(get_neighbors(i, j, board))
                if board[i, j] == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                    new_board[i, j] = 1
                elif board[i, j] == 0 and alive_neighbors == 3:
                    new_board[i, j] = 1
        return new_board

    for _ in range(iterations):
        board = next_generation(board)
    return board

# Example usage:
initial_board = np.array([[0, 1, 0],
                          [0, 1, 0],
                          [0, 1, 0]])

print("Initial Board:")
print(initial_board)

final_board = game_of_life(initial_board, 10)
print("Final Board after 10 iterations:")
print(final_board)