def solve_sudoku(puzzle):
    def is_valid(row, col, num):
        for i in range(9):
            if puzzle[row][i] == num or puzzle[i][col] == num:
                return False

        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if puzzle[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve():
        row, col = -1, -1
        empty = False
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    row, col = i, j
                    empty = True
                    break
            if empty:
                break

        if not empty:
            return True

        for num in range(1, 10):
            if is_valid(row, col, num):
                puzzle[row][col] = num
                if solve():
                    return True
            puzzle[row][col] = 0
        return False

    if solve():
        return puzzle
    else:
        return "No solution exists"


sudoku_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

solution = solve_sudoku(sudoku_puzzle)
for row in solution:
    print(row)