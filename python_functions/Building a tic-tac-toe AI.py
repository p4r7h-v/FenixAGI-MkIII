def tic_tac_toe_ai(board, player):
    def empty_cells(board):
        return [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]

    def is_winner(board, player):
        for row in board:
            if row == [player, player, player]: return True
        for col in range(3):
            if [board[r][col] for r in range(3)] == [player, player, player]: return True
        if [board[i][i] for i in range(3)] == [player, player, player]: return True
        if [board[i][2 - i] for i in range(3)] == [player, player, player]: return True

        return False

    def minimax(board, depth, maximizing_player):
        if is_winner(board, 1): return -1
        if is_winner(board, 2): return 1
        if not empty_cells(board): return 0

        if maximizing_player:
            max_eval = float('-inf')
            for r, c in empty_cells(board):
                board[r][c] = 2
                eval = minimax(board, depth + 1, False)
                board[r][c] = 0
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for r, c in empty_cells(board):
                board[r][c] = 1
                eval = minimax(board, depth + 1, True)
                board[r][c] = 0
                min_eval = min(min_eval, eval)
            return min_eval

    best_move = None
    best_value = float('-inf')

    for r, c in empty_cells(board):
        board[r][c] = player
        move_value = minimax(board, 0, False)
        board[r][c] = 0
        if move_value > best_value:
            best_value = move_value
            best_move = (r, c)

    return best_move