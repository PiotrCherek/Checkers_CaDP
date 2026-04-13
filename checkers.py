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
        piece = self.board[row][col]
        if piece is None:
            return False
        return self.current_player in piece

    def square_exists(self, row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def promote_pawn(self, row: int, col: int) -> None:
        """Promotes a pawn to a King if it reaches the opposite side."""
        if self.current_player == "White" and row == 0:
            self.board[row][col] = "White_King"
        elif self.current_player == "Black" and row == 7:
            self.board[row][col] = "Black_King"

    def move_legal(self, row: int, col: int) -> bool:
        if not self.selected_piece or not self.square_exists(row, col):
            return False
        if self.board[row][col] is not None: 
            return False

        from_r, from_c = self.selected_piece
        piece = self.board[from_r][from_c]
        row_diff, col_diff = row - from_r, col - from_c
        abs_r, abs_c = abs(row_diff), abs(col_diff)

        if abs_r != abs_c: return False 

        if "King" in piece:
            step_r = 1 if row_diff > 0 else -1
            step_c = 1 if col_diff > 0 else -1
            enemy_count = 0
            
            for i in range(1, abs_r):
                mid_p = self.board[from_r + i*step_r][from_c + i*step_c]
                if mid_p is not None:
                    if self.current_player in mid_p: return False # Blocked by friend
                    enemy_count += 1
            return enemy_count <= 1 # Legal if 0 enemies (slide) or 1 enemy (jump)
        else:
            # PAWN LOGIC
            if abs_c == 1: # Normal move
                if piece == "White" and row_diff == -1: return True
                if piece == "Black" and row_diff == 1: return True
            if abs_c == 2 and abs_r == 2: # Jump
                mid_r, mid_c = (from_r + row) // 2, (from_c + col) // 2
                mid_p = self.board[mid_r][mid_c]
                enemy = "Black" if piece == "White" else "White"
                if mid_p and enemy in mid_p:
                    return True
        return False

    
    def can_capture_more(self, row: int, col: int) -> bool:
        piece = self.board[row][col]
        if not piece: return False
        old_sel = self.selected_piece
        self.selected_piece = (row, col)
        
        can_jump = False
        max_range = 8 if "King" in piece else 3
        
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            enemy_count = 0
            for dist in range(1, max_range):
                tr, tc = row + dr*dist, col + dc*dist
                if not self.square_exists(tr, tc):
                    break # OUT OF BOARD
                
                target = self.board[tr][tc]
                if target is not None:
                    if self.current_player in target:
                        break 
                    else:
                        enemy_count += 1
                        if enemy_count > 1:
                            break # TWO PAWN 
                
                if self.move_legal(tr, tc):
                    if self.is_capture_path_logic(row, col, tr, tc):
                        can_jump = True
                        break
            if can_jump: break

        self.selected_piece = old_sel
        return can_jump
    
    
    def is_capture_path_logic(self, sr, sc, er, ec):
        step_r = 1 if er > sr else -1
        step_c = 1 if ec > sc else -1
        curr_r, curr_c = sr + step_r, sc + step_c
        while (curr_r, curr_c) != (er, ec):
            if self.board[curr_r][curr_c] is not None:
                return True # Found a piece to jump
            curr_r += step_r
            curr_c += step_c
        return False

    def move_piece(self, row: int, col: int) -> bool:
        from_row, from_col = self.selected_piece
        piece = self.board[from_row][from_col]
        had_capture = False

        step_r = 1 if row > from_row else -1
        step_c = 1 if col > from_col else -1
        
        curr_r, curr_c = from_row + step_r, from_col + step_c
        while (curr_r, curr_c) != (row, col):
            if self.board[curr_r][curr_c] is not None:
                self.board[curr_r][curr_c] = None 
                had_capture = True
            curr_r += step_r
            curr_c += step_c

        self.board[row][col] = piece
        self.board[from_row][from_col] = None
        self.promote_pawn(row, col)
        
        return had_capture

    def get_all_mandatory_jumps(self) -> list:
        """Returns a list of (row, col) coordinates of pieces that MUST jump."""
        mandatory_pieces = []
        for r in range(8):
            for c in range(8):
                if self.own_piece_selected(r, c):
                    if self.can_capture_more(r, c):
                        mandatory_pieces.append((r, c))
        return mandatory_pieces

    def handle_click(self, row: int, col: int) -> None:
        mandatory = self.get_all_mandatory_jumps()

        if self.own_piece_selected(row, col):
            if mandatory and (row, col) not in mandatory: return
            self.selected_piece = (row, col)
            return

        if self.selected_piece and self.move_legal(row, col):
            # NEW KING-AWARE CAPTURE CHECK
            is_cap = self.is_capture_path_logic(self.selected_piece[0], self.selected_piece[1], row, col)
            
            if mandatory and not is_cap:
                print("You must take the enemy piece!")
                return

            had_capture = self.move_piece(row, col)

            if had_capture and self.can_capture_more(row, col):
                self.selected_piece = (row, col)
            else:
                self.selected_piece = None
                self.current_player = "Black" if self.current_player == "White" else "White"