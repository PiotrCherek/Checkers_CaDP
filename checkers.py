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

    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> None:
        piece = self.board[from_row][from_col]
        if piece is None:
            raise ValueError("No piece at the source position")
        if self.board[to_row][to_col] is not None:
            raise ValueError("Destination position is not empty")
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

    def handle_click(self, row: int, col: int) -> None:
        if self.selected_piece is None:
            if self.board[row][col] is not None and self.board[row][col] == self.current_player:
                self.selected_piece = (row, col)