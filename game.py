import pygame
import checkers as ck
from network import Network

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.running = True

        self.checkers = ck.Checkers()
        
        self.network = Network()
        self.my_color = self.network.color
        pygame.display.set_caption(f"Warcaby - Jesteś graczem: {self.my_color}")
        
        self.last_network_sync = 0
        self.sync_interval = 100 

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
                    piece_color = (255, 255, 255) if "White" in piece else (20, 20, 20)
                    center = (col * 100 + 50, row * 100 + 50)
                    
                    pygame.draw.circle(self.screen, piece_color, center, 40)
                    
                    if "King" in piece:
                        pygame.draw.circle(self.screen, (255, 215, 0), center, 40, 5)
                        pygame.draw.circle(self.screen, (255, 215, 0), center, 15)

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
                enemy_count = 0
                for dist in range(1, 8):
                    tr, tc = current_row + dr * dist, current_col + dc * dist
                    if not self.checkers.square_exists(tr, tc):
                        break
                    
                    target = self.checkers.board[tr][tc]
                    if target is not None:
                        if self.checkers.current_player in target:
                            break 
                        else:
                            enemy_count += 1
                            if enemy_count > 1:
                                break 

                    if self.checkers.move_legal(tr, tc):
                        if mandatory:
                            if not self.is_path_capture(current_row, current_col, tr, tc):
                                continue 
                        pygame.draw.circle(self.screen, (0, 255, 0), (tc * 100 + 50, tr * 100 + 50), 15)
            return 

        if mandatory:
            directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        else:
            directions = [(-1, -1), (-1, 1)] if piece == "White" else [(1, 1), (1, -1)]
            
        for dr, dc in directions:
            to_row, to_col = current_row + dr, current_col + dc
            if self.checkers.square_exists(to_row, to_col) and self.checkers.move_legal(to_row, to_col):
                pygame.draw.circle(self.screen, (0, 255, 0), (to_col * 100 + 50, to_row * 100 + 50), 15)

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

    def show_board(self, selected_piece: tuple) -> None:
        self.screen.fill((0, 0, 0))
        self.draw_board()
        
        mandatory = self.checkers.get_all_mandatory_jumps()
        for r, c in mandatory:
            pygame.draw.rect(self.screen, (255, 255, 0), (c * 100, r * 100, 100, 100), 5)

        self.draw_pieces()

        if selected_piece:
            self.show_selected_piece(selected_piece)
            self.draw_possible_moves(selected_piece)

    def run(self) -> None:
        while self.running:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.last_network_sync > self.sync_interval:
                self.last_network_sync = current_time
                try:
                    server_state = self.network.send({"type": "GET"})
                    
                    if server_state and server_state.get("board") is not None:
                        self.checkers.board = server_state["board"]
                        self.checkers.current_player = server_state["current_player"]
                except Exception as e:
                    pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.checkers.current_player == self.my_color:
                        x, y = event.pos
                        col, row = x // 100, y // 100
                        
                        old_player = self.checkers.current_player
                        
                        self.checkers.handle_click(row, col)
                        
                        if self.checkers.current_player != old_player:
                            self.network.send({
                                "type": "UPDATE",
                                "board": self.checkers.board,
                                "current_player": self.checkers.current_player
                            })

            self.show_board(self.checkers.selected_piece)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()