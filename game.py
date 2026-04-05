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
                    # Determine base color
                    piece_color = (255, 255, 255) if "White" in piece else (20, 20, 20)
                    center = (col * 100 + 50, row * 100 + 50)
                    
                    # Draw main piece
                    pygame.draw.circle(self.screen, piece_color, center, 40)
                    
                    # If it's a King, add a unique visual (Gold Crown/Ring)
                    if "King" in piece:
                        pygame.draw.circle(self.screen, (255, 215, 0), center, 40, 5) # Gold border
                        pygame.draw.circle(self.screen, (255, 215, 0), center, 15)    # Gold center

    def show_selected_piece(self, selected_piece: tuple) -> None:
        if not selected_piece:
            return

        highlight_color = (255, 0, 255) if self.checkers.current_player == "White" else (255, 255, 0)

        row, col = selected_piece
        pygame.draw.circle(self.screen, highlight_color, (col * 100 + 50, row * 100 + 50), 45, 5)

    def draw_possible_moves(self, selected_piece: tuple) -> None:
        current_row, current_col = selected_piece
        piece = self.checkers.board[current_row][current_col]
        
        if piece is None: return
        
        mandatory = self.checkers.get_all_mandatory_jumps()

        if "King" in piece:
            for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                for dist in range(1, 8):
                    tr, tc = current_row + dr * dist, current_col + dc * dist
                    if self.checkers.square_exists(tr, tc) and self.checkers.move_legal(tr, tc):
                        # If mandatory jumps exist, only draw the move if it's actually a capture
                        if mandatory:
                            # Check if this specific sliding move jumps an enemy
                            if not self.is_path_capture(current_row, current_col, tr, tc):
                                continue 
                        pygame.draw.circle(self.screen, (0, 255, 0), (tc * 100 + 50, tr * 100 + 50), 15)
                    else:
                        break 
            return 
        if mandatory:
            directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        else:
            directions = [(-1, -1), (-1, 1)] if piece == "White" else [(1, 1), (1, -1)]
        for dr, dc in directions:
            to_row, to_col = current_row + dr, current_col + dc
            if self.checkers.square_exists(to_row, to_col) and self.checkers.move_legal(to_row, to_col):
                pygame.draw.circle(self.screen, (0, 255, 0), (to_col * 100 + 50, to_row * 100 + 50), 15)

    def show_board(self, selected_piece: tuple) -> None:
        self.screen.fill((0, 0, 0))
        self.draw_board()
        
        # Visual cue for mandatory jumps
        mandatory = self.checkers.get_all_mandatory_jumps()
        for r, c in mandatory:
            pygame.draw.rect(self.screen, (255, 255, 0), (c * 100, r * 100, 100, 100), 5)

        self.draw_pieces()

        if selected_piece:
            self.show_selected_piece(selected_piece)
            self.draw_possible_moves(selected_piece)

    def is_path_capture(self, start_row, start_col, end_row, end_col) -> bool:
        step_r = 1 if end_row > start_row else -1
        step_c = 1 if end_col > start_col else -1
        
        curr_r, curr_c = start_row + step_r, start_col + step_c
        while (curr_r, curr_c) != (end_row, end_col):
            if self.checkers.board[curr_r][curr_c] is not None:
                enemy = "Black" if self.checkers.current_player == "White" else "White"
                if enemy in self.checkers.board[curr_r][curr_c]:
                    return True
            curr_r += step_r
            curr_c += step_c
        return False

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