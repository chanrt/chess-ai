import numpy as np

from constants import consts as c


def inside_board(mouse_pos):
    x, y = mouse_pos
    return c.board_x < x < c.board_x + c.board_length and c.board_y < y < c.board_y + c.board_length


def get_click_coords(mouse_pos):
    x, y = mouse_pos
    x -= c.board_x
    y -= c.board_y
    row = int(y / c.square_length)
    col = int(x / c.square_length)
    return row, col


def get_move_coords(click_coords, legal_moves):
    move_coords_list = []
    for move in legal_moves:
        if move[0] == click_coords:
            move_coords_list.append(move[1])
    return move_coords_list


def clicked_self(board, coords, color):
    if color == "white" and board[coords] > 0:
        return True
    elif color == "black" and board[coords] < 0:
        return True
    else:
        return False


def is_legal_move(coords, move_coords_list):
    for move_coords in move_coords_list:
        if coords == move_coords:
            return move_coords
    return None


def init_board():
    board = np.zeros((8, 8), dtype=int)

    # white pieces
    board[6][:] = 1
    board[7][1] = board[7][6] = 2
    board[7][2] = board[7][5] = 3
    board[7][0] = board[7][7] = 4
    board[7][3] = 5
    board[7][4] = 6

    # black pieces
    board[1][:] = -1
    board[0][1] = board[0][6] = -2
    board[0][2] = board[0][5] = -3
    board[0][0] = board[0][7] = -4
    board[0][3] = -5
    board[0][4] = -6

    return board