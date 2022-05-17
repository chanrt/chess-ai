from math import floor

from constants import consts as c


class CapturedPieceManager:
    def __init__(self, images, color, screen):
        self.images = images
        self.color = color
        self.screen = screen

        self.captured_pieces = []
        self.x = []
        self.y = []

    def add_piece(self, piece):
        num_pieces = len(self.captured_pieces)
        row = floor(num_pieces / 3)
        col = num_pieces % 3

        if self.color == "white":
            self.x.append((col + 0.25) * c.piece_spacing_x)
            self.y.append(c.board_y + (row + 0.25) * c.piece_spacing_y)
        elif self.color == "black":
            self.x.append(c.board_x + c.board_length + (col + 0.25) * c.piece_spacing_x)
            self.y.append(c.board_y + (row + 0.25) * c.piece_spacing_y)
        self.captured_pieces.append(self.get_image(piece))

    def render(self):
        for i in range(len(self.captured_pieces)):
            self.screen.blit(self.captured_pieces[i], (self.x[i], self.y[i]))

    def reset(self):
        self.captured_pieces = []
        self.x = []
        self.y = []

    def get_image(self, piece):
        image = None
        if piece == 1:
            image = self.images.white_pawn
        elif piece == -1:
            image = self.images.black_pawn
        elif piece == 2:
            image = self.images.white_knight
        elif piece == -2:
            image = self.images.black_knight
        elif piece == 3:
            image = self.images.white_bishop
        elif piece == -3:
            image = self.images.black_bishop
        elif piece == 4:
            image = self.images.white_rook
        elif piece == -4:
            image = self.images.black_rook
        elif piece == 5:
            image = self.images.white_queen
        elif piece == -5:
            image = self.images.black_queen
        elif piece == 6:
            image = self.images.white_king
        elif piece == -6:
            image = self.images.black_king
        return image

    def get_num_pawns(self, board):
        num_pawns = 0
        for row in range(8):
            for col in range(8):
                if self.color == "white" and board[row][col] == 1:
                    num_pawns += 1
                elif self.color == "black" and board[row][col] == -1:
                    num_pawns += 1
        return num_pawns

    def get_num_knights(self, board):
        num_knights = 0
        for row in range(8):
            for col in range(8):
                if self.color == "white" and board[row][col] == 2:
                    num_knights += 1
                elif self.color == "black" and board[row][col] == -2:
                    num_knights += 1
        return num_knights

    def get_num_bishops(self, board):
        num_bishops = 0
        for row in range(8):
            for col in range(8):
                if self.color == "white" and board[row][col] == 3:
                    num_bishops += 1
                elif self.color == "black" and board[row][col] == -3:
                    num_bishops += 1
        return num_bishops

    def get_num_rooks(self, board):
        num_rooks = 0
        for row in range(8):
            for col in range(8):
                if self.color == "white" and board[row][col] == 4:
                    num_rooks += 1
                elif self.color == "black" and board[row][col] == -4:
                    num_rooks += 1
        return num_rooks

    def get_num_queens(self, board):
        num_queens = 0
        for row in range(8):
            for col in range(8):
                if self.color == "white" and board[row][col] == 5:
                    num_queens += 1
                elif self.color == "black" and board[row][col] == -5:
                    num_queens += 1
        return num_queens

    def get_captured_pieces(self, board):
        self.reset()

        num_pawns = self.get_num_pawns(board)
        num_knights = self.get_num_knights(board)
        num_bishops = self.get_num_bishops(board)
        num_rooks = self.get_num_rooks(board)
        num_queens = self.get_num_queens(board)

        for _ in range(8 - num_pawns):
            if self.color == "white":
                self.add_piece(1)
            elif self.color == "black":
                self.add_piece(-1)

        for _ in range(2 - num_knights):
            if self.color == "white":
                self.add_piece(2)
            elif self.color == "black":
                self.add_piece(-2)
        
        for i in range(2 - num_bishops):
            if self.color == "white":
                self.add_piece(3)
            elif self.color == "black":
                self.add_piece(-3)

        for _ in range(2 - num_rooks):
            if self.color == "white":
                self.add_piece(4)
            elif self.color == "black":
                self.add_piece(-4)

        for _ in range(1 - num_queens):
            if self.color == "white":
                self.add_piece(5)
            elif self.color == "black":
                self.add_piece(-5)