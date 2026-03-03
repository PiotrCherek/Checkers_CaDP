import pygame

class Checkers:
    def __init__(self) -> None:
        self.board = self.init_board()
        self.selected_piece = None
        self.current_player = "White"

    def init_board(self) -> list:
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

    def own_piece_selected(self, row: int, col: int) -> bool:
        return self.board[row][col] is not None and self.board[row][col] == self.current_player

    def square_exists(self, row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def move_legal(self, row: int, col: int) -> bool:
        from_row, from_col = self.selected_piece
        piece = self.board[from_row][from_col]

        if piece is None:
            return False

        if self.board[row][col] is not None:
            return False

        row_diff = row - from_row
        col_diff = col - from_col

        if piece == "White":
            return row_diff == -1 and abs(col_diff) == 1
        else:  # Black
            return row_diff == 1 and abs(col_diff) == 1

    def move_piece(self, row: int, col: int) -> None:
        from_row, from_col = self.selected_piece
        self.board[from_row][from_col] = None
        self.board[row][col] = self.current_player
        self.selected_piece = None

    def handle_click(self, row: int, col: int) -> None:
        if self.own_piece_selected(row, col):
            self.selected_piece = (row, col)
            return

        if self.selected_piece is None:
            return

        if self.move_legal(row, col):
            self.move_piece(row, col)
            self.current_player = "Black" if self.current_player == "White" else "White"