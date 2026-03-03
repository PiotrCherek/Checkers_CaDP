import pygame
import checkers as ck

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Checkers")
        self.clock = pygame.time.Clock()
        self.running = True

        self.checkers = ck.Checkers()

    def draw_board(self) -> None:
        for row in range(8):
            for col in range(8):
                color = (255, 0, 0) if (row + col) % 2 == 0 else (0, 0, 255)
                pygame.draw.rect(self.screen, color, (col * 100, row * 100, 100, 100))

    def draw_pieces(self) -> None:
        for row in range(8):
            for col in range(8):
                piece = self.checkers.board[row][col]
                if piece is not None:
                    piece_color = (255, 255, 255) if piece == "White" else (0, 0, 0)
                    pygame.draw.circle(self.screen, piece_color, (col * 100 + 50, row * 100 + 50), 40)

    def show_selected_piece(self, selected_piece: tuple) -> None:
        if not selected_piece:
            return

        highlight_color = (255, 0, 255) if self.checkers.current_player == "White" else (255, 255, 0)

        row, col = selected_piece
        pygame.draw.circle(self.screen, highlight_color, (col * 100 + 50, row * 100 + 50), 45, 5)

    def draw_possible_moves(self, selected_piece: tuple) -> None:
        current_row, current_col = selected_piece
        piece = self.checkers.board[current_row][current_col]

        if piece is None:
            return

        directions = [(-1, -1), (-1, 1)] if piece == "White" else [(1, 1), (1, -1)]
        highlight_color = (255, 0, 255) if self.checkers.current_player == "White" else (255, 255, 0)

        for dr, dc in directions:
            to_row, to_col = current_row + dr, current_col + dc
            if self.checkers.square_exists(to_row, to_col) and self.checkers.move_legal(to_row, to_col):
                pygame.draw.circle(self.screen, highlight_color, (to_col * 100 + 50, to_row * 100 + 50), 10)

    def show_board(self, selected_piece: tuple) -> None:
        self.screen.fill((0, 0, 0))
        self.draw_board()
        self.draw_pieces()

        if selected_piece:
            self.show_selected_piece(selected_piece)
            self.draw_possible_moves(selected_piece)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col, row = x // 100, y // 100
                    self.checkers.handle_click(row, col)

            self.show_board(self.checkers.selected_piece)
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()