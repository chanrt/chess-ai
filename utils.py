import numpy as np

from constants import consts as c
from moves import get_legal_moves, get_king_pos


def get_targeted_squares(board, color):
    targeted_squares = []
    player_multiplier = 1 if color == "white" else -1
    enemy_color = "white" if color == "black" else "black"
    enemy_moves = get_legal_moves(board, enemy_color, True)

    for row in range(8):
        for col in range(8):
            if board[row][col] * player_multiplier > 0:
                for move in enemy_moves:
                    if move[1] == (row, col):
                        targeted_squares.append((row, col))
                        break
    return targeted_squares


def is_castling_move(board, move, color):
    row = 7 if color == "white" else 0
    multiplier = 1 if color == "white" else -1

    if move[0] == (row, 4) and board[move[1]] == 6 * multiplier:
        if move[1] == (row, 6):
            return 1
        elif move[1] == (row, 2):
            return 2
    return None


def check_castling(board, board_record, color):
    castling_moves = []
    row = 7 if color == "white" else 0
    multiplier = 1 if color == "white" else -1

    if (not any(board[row][5:7]) or not any(board[row][1:4])) and not is_player_in_check(board, color):
        king_rook_moved = False
        for every_board in board_record:
            if every_board[row][7] != 4 * multiplier:
                king_rook_moved = True
                break

        queen_rook_moved = False
        for every_board in board_record:
            if every_board[row][0] != 4 * multiplier:
                queen_rook_moved = True
                break

        king_moved = False
        for every_board in board_record:
            if every_board[row][4] != 6 * multiplier:
                king_moved = True
                break

        if not king_moved:
            enemy_color = "white" if color == "black" else "black"
            enemy_legal_moves = get_legal_moves(board, enemy_color, True)

            if not king_rook_moved and not any(board[row][5:7]):
                squares_to_check = [(row, 5), (row, 6)]

                legal = True
                for enemy_move in enemy_legal_moves:
                    for square in squares_to_check:
                        if square == enemy_move:
                            legal = False
                            break
                
                if legal == True:
                    castling_moves.append([(row, 4), (row, 6)])

            if not queen_rook_moved and not any(board[row][1:4]):
                squares_to_check = [(row, 1), (row, 2), (row, 3)]

                legal = True
                for enemy_move in enemy_legal_moves:
                    for square in squares_to_check:
                        if square == enemy_move:
                            legal = False
                            break
                
                if legal == True:
                    castling_moves.append([(row, 4), (row, 2)])

    return castling_moves


def check_promotions(board):
    for col in range(8):
        if board[0][col] == 1:
            board[0][col] = 5
            c.promote_sound.play()
    
    for col in range(8):
        if board[0][col] == -1:
            board[0][col] = -5
            c.promote_sound.play()


def is_player_in_check(board, color):
    enemy_color = "white" if color == "black" else "black"
    enemy_legal_moves = get_legal_moves(board, enemy_color, True)

    for move in enemy_legal_moves:
        if move[1] == get_king_pos(board, color):
            return True
    return False


def is_enemy_in_check(board, color):
    enemy_color = "white" if color == "black" else "black"
    return is_player_in_check(board, enemy_color)


def make_move_commons(board, move):
    board[move[1]] = board[move[0]]
    board[move[0]] = 0


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