import pygame
import checkers as ck

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Checkers")
        self.clock = pygame.time.Clock()
        self.running = True

        self.checkers = ck.Checkers()

    def show_board(self):
        for row in range(8):
            for col in range(8):
                color = (255, 0, 0) if (row + col) % 2 == 0 else (0, 0, 255)
                pygame.draw.rect(self.screen, color, (col * 100, row * 100, 100, 100))

                piece = self.checkers.board[row][col]
                if piece is not None:
                    piece_color = (255, 255, 255) if piece == "White" else (0, 0, 0)
                    pygame.draw.circle(self.screen, piece_color, (col * 100 + 50, row * 100 + 50), 40)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.show_board()
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()