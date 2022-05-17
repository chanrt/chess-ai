from numba import njit

from moves import get_legal_moves


@njit(nogil=True)
def in_center(row, col):
    return 2 < row < 5 and 2 < col < 5


@njit(nogil=True)
def evaluate(board):
    white_score = 0
    black_score = 0

    pawn_material, pawn_center = 1, 1
    knight_material, knight_center = 3, 3
    bishop_material, bishop_center = 4, 3
    rook_material, rook_center = 5, 3
    queen_material, queen_center = 9, 6

    for row in range(8):
        for col in range(8):
            # pawn
            if board[row][col] == 1:
                white_score += pawn_material
                if 2 < row < 5 and 2 < col < 5:
                    white_score += pawn_center
            elif board[row][col] == -1:
                black_score += pawn_material
                if 2 < row < 5 and 2 < col < 5:
                    black_score += pawn_center

            # knight
            elif board[row][col] == 2:
                white_score += knight_material
                if 2 < row < 5 and 2 < col < 5:
                    white_score += knight_center
            elif board[row][col] == -2:
                black_score += knight_material
                if 2 < row < 5 and 2 < col < 5:
                    black_score += knight_center

            # bishop
            elif board[row][col] == 3:
                white_score += bishop_material
                if 2 < row < 5 and 2 < col < 5:
                    white_score += bishop_center
            elif board[row][col] == -3:
                black_score += bishop_material
                if 2 < row < 5 and 2 < col < 5:
                    black_score += bishop_center

            # rook
            elif board[row][col] == 4:
                white_score += rook_material
                if 2 < row < 5 and 2 < col < 5:
                    white_score += rook_center
            elif board[row][col] == -4:
                black_score += rook_material
                if 2 < row < 5 and 2 < col < 5:
                    black_score += rook_center

            # queen
            elif board[row][col] == 5:
                white_score += queen_material
                if 2 < row < 5 and 2 < col < 5:
                    white_score += queen_center
            elif board[row][col] == -5:
                black_score += queen_material
                if 2 < row < 5 and 2 < col < 5:
                    black_score += queen_center
    
    return white_score - black_score