def chess_game():
    pieces = {
        "R": "Rook",
        "N": "Knight",
        "B": "Bishop",
        "Q": "Queen",
        "K": "King",
        "P": "Pawn"
    }
    white_pieces = {k: "\u2654" if k == "K" else "\u2655" if k == "Q" else "\u2656" if k == "R" else
                    "\u2657" if k == "B" else "\u2658" if k == "N" else "\u2659" for k in pieces.keys()}
    black_pieces = {k: "\u265A" if k == "K" else "\u265B" if k == "Q" else "\u265C" if k == "R" else
                    "\u265D" if k == "B" else "\u265E" if k == "N" else "\u265F" for k in pieces.keys()}
  
    chessboard = [
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        [" " for _ in range(8)],
        [" " for _ in range(8)],
        [" " for _ in range(8)],
        [" " for _ in range(8)],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["r", "n", "b", "q", "k", "b", "n", "r"]
    ]

    def print_board(board):
        print("  a b c d e f g h")
        for row, line in enumerate(board):
            print(8 - row, end=" ")
            for piece in line:
                print(white_pieces[piece.upper()] if piece.isupper() else black_pieces[piece.upper()] if piece.islower() else piece, end=" ")
            print(8 - row)
        print("  a b c d e f g h")

    print_board(chessboard)
    
    # Add your implementation for actual game play, such as move validation, player input, and game loop

chess_game()