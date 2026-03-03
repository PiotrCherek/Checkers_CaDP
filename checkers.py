class Checkers:
    def __init__(self):
        self.board = self.init_board()

    def init_board(self):
        """Create an 8x8 board with pieces in starting positions"""

        board = [[None for _ in range(8)] for _ in range(8)]

        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = "Black"

        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = "White"
        return board

    def move_piece(self, from_row, from_col, to_row, to_col):
        # Move a piece from one position to another
        piece = self.board[from_row][from_col]
        if piece is None:
            raise ValueError("No piece at the source position")
        if self.board[to_row][to_col] is not None:
            raise ValueError("Destination position is not empty")
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None