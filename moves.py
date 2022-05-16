from numba import njit
import numpy as np


@njit(nogil=True)
def can_move_to(board, piece, row, col):
    return (-1 < row < 8 and -1 < col < 8) and (board[row][col] == 0 or piece * board[row][col] < 0)


@njit(nogil=True)
def get_king_pos(board, color):
    for row in range(8):
        for col in range(8):
            if board[row][col] == 6 and color == "white":
                return (row, col)
            elif board[row][col] == -6 and color == "black":
                return (row, col)


@njit(nogil=True)
def make_move(board, move):
    board[move[1]] = board[move[0]]
    board[move[0]] = 0


@njit(nogil=True)
def get_pawn_moves(board, row, col, color):
    pawn_moves = []

    if color == "white":
        if row > 0 and board[row - 1][col] == 0:
            pawn_moves.append([(row, col), (row - 1, col)])
            if row == 6 and board[row - 2][col] == 0:
                pawn_moves.append([(row, col), (row - 2, col)])
        if col > 0 and board[row - 1][col - 1] < 0:
            pawn_moves.append([(row, col), (row - 1, col - 1)])
        if col < 7 and board[row - 1][col + 1] < 0:
            pawn_moves.append([(row, col), (row - 1, col + 1)])
    else:
        if row < 7 and board[row + 1][col] == 0:
            pawn_moves.append([(row, col), (row + 1, col)])
            if row == 1 and board[row + 2][col] == 0:
                pawn_moves.append([(row, col), (row + 2, col)])
        if col > 0 and board[row + 1][col - 1] > 0:
            pawn_moves.append([(row, col), (row + 1, col - 1)])
        if col < 7 and board[row + 1][col + 1] > 0:
            pawn_moves.append([(row, col), (row + 1, col + 1)])

    return pawn_moves


@njit(nogil=True)
def get_knight_moves(board, row, col):
    piece = board[row][col]
    knight_moves = []

    if can_move_to(board, piece, row - 1, col - 2):
        knight_moves.append([(row, col), (row - 1, col - 2)])
    if can_move_to(board, piece, row - 1, col + 2):
        knight_moves.append([(row, col), (row - 1, col + 2)])
    if can_move_to(board, piece, row + 1, col - 2):
        knight_moves.append([(row, col), (row + 1, col - 2)])
    if can_move_to(board, piece, row + 1, col + 2):
        knight_moves.append([(row, col), (row + 1, col + 2)])
    if can_move_to(board, piece, row - 2, col - 1):
        knight_moves.append([(row, col), (row - 2, col - 1)])
    if can_move_to(board, piece, row - 2, col + 1):
        knight_moves.append([(row, col), (row - 2, col + 1)])
    if can_move_to(board, piece, row + 2, col - 1):
        knight_moves.append([(row, col), (row + 2, col - 1)])
    if can_move_to(board, piece, row + 2, col + 1):
        knight_moves.append([(row, col), (row + 2, col + 1)])

    return knight_moves


@njit(nogil=True)
def get_bishop_moves(board, row, col):
    piece = board[row][col]
    bishop_moves = []

    for drow in [-1, 1]:
        for dcol in [-1, 1]:
            cur_row = row + drow
            cur_col = col + dcol
            while -1 < cur_row < 8 and -1 < cur_col < 8:
                if piece * board[cur_row][cur_col] > 0:
                    break
                elif piece * board[cur_row][cur_col] < 0:
                    bishop_moves.append([(row, col), (cur_row, cur_col)])
                    break
                else:
                    bishop_moves.append([(row, col), (cur_row, cur_col)])
                cur_row += drow
                cur_col += dcol

    return bishop_moves


@njit(nogil=True)
def get_rook_moves(board, row, col):
    piece = board[row][col]
    rook_moves = []

    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            if drow * dcol == 0 and drow != dcol:
                cur_row = row + drow
                cur_col = col + dcol
                while -1 < cur_row < 8 and -1 < cur_col < 8:
                    if piece * board[cur_row][cur_col] > 0:
                        break
                    elif piece * board[cur_row][cur_col] < 0:
                        rook_moves.append([(row, col), (cur_row, cur_col)])
                        break
                    else:
                        rook_moves.append([(row, col), (cur_row, cur_col)])
                    cur_row += drow
                    cur_col += dcol

    return rook_moves


@njit(nogil=True)
def get_queen_moves(board, row, col):
    piece = board[row][col]
    queen_moves = []

    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            if not (drow == 0 and dcol == 0):
                cur_row = row + drow
                cur_col = col + dcol
                while -1 < cur_row < 8 and -1 < cur_col < 8:
                    if piece * board[cur_row][cur_col] > 0:
                        break
                    elif piece * board[cur_row][cur_col] < 0:
                        queen_moves.append([(row, col), (cur_row, cur_col)])
                        break
                    else:
                        queen_moves.append([(row, col), (cur_row, cur_col)])
                    cur_row += drow
                    cur_col += dcol

    return queen_moves


@njit(nogil=True)
def get_king_moves(board, row, col):
    king_moves = []

    if can_move_to(board, board[row][col], row - 1, col - 1):
        king_moves.append([(row, col), (row - 1, col - 1)])
    if can_move_to(board, board[row][col], row - 1, col):
        king_moves.append([(row, col), (row - 1, col)])
    if can_move_to(board, board[row][col], row - 1, col + 1):
        king_moves.append([(row, col), (row - 1, col + 1)])
    if can_move_to(board, board[row][col], row, col - 1):
        king_moves.append([(row, col), (row, col - 1)])
    if can_move_to(board, board[row][col], row, col + 1):
        king_moves.append([(row, col), (row, col + 1)])
    if can_move_to(board, board[row][col], row + 1, col - 1):
        king_moves.append([(row, col), (row + 1, col - 1)])
    if can_move_to(board, board[row][col], row + 1, col):
        king_moves.append([(row, col), (row + 1, col)])
    if can_move_to(board, board[row][col], row + 1, col + 1):
        king_moves.append([(row, col), (row + 1, col + 1)])

    return king_moves


@njit(nogil=True)
def get_legal_moves(board, color, current=False):
    moves = []

    for row in range(8):
        for col in range(8):
            if board[row][col] > 0 and color == "white" or board[row][col] < 0 and color == "black":
                piece = abs(board[row][col])
                if piece == 1:
                    moves.extend(get_pawn_moves(board, row, col, color))
                elif piece == 2:
                    moves.extend(get_knight_moves(board, row, col))
                elif piece == 3:
                    moves.extend(get_bishop_moves(board, row, col))
                elif piece == 4:
                    moves.extend(get_rook_moves(board, row, col))
                elif piece == 5:
                    moves.extend(get_queen_moves(board, row, col))
                elif piece == 6:
                    moves.extend(get_king_moves(board, row, col))

    if current:
        illegal_moves = []
        
        for move in moves:
            temp_board = np.copy(board)
            make_move(temp_board, move)
            enemy_color = "black" if color == "white" else "white"
            enemy_legal_moves = get_legal_moves(temp_board, enemy_color, False)
            player_king_pos = get_king_pos(temp_board, color)

            for enemy_move in enemy_legal_moves:
                if enemy_move[1] == player_king_pos:
                    illegal_moves.append(move)
                    break

        for illegal_move in illegal_moves:
            moves.remove(illegal_move)

    return moves