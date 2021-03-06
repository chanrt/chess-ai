from itertools import product
import pygame as pg

from constants import consts as c


def draw_everything(board, img, screen):
    screen.fill(c.bg_color)
    draw_background(screen)
    draw_clicked(c.click_coords, c.chance, screen)
    draw_board(board, img, c.chance, screen)
    draw_move_coords(c.move_coords_list, c.chance, screen)
    draw_ai_move(c.ai_move, screen)
    draw_targeted_squares(c.targeted_squares, screen)

    c.title_text.render()
    c.white_captured_pieces.render()
    c.black_captured_pieces.render()
    c.restart_button.render()
    c.quit_button.render()


def draw_background(screen):
    for row, col in product(range(8), range(8)):
        if (row + col) % 2 == 1:
            square_color = c.black_color
        else:
            square_color = c.white_color
        x = c.board_x + col * c.square_length
        y = c.board_y + row * c.square_length
        rect = pg.Rect(x, y, c.square_length, c.square_length)
        pg.draw.rect(screen, square_color, rect)


def draw_clicked(click_coords, chance, screen):
    if click_coords is not None:
        row, col = click_coords
        if chance == "white":
            act_row, act_col = row, col
        else:
            act_row, act_col = 7 - row, 7 - col

        x = c.board_x + act_col * c.square_length
        y = c.board_y + act_row * c.square_length
        rect = pg.Rect(x, y, c.square_length, c.square_length)
        pg.draw.rect(screen, c.selected_color, rect)


def draw_board(board, img, color, screen):
    for row, col in product(range(8), range(8)):
        if board[row][col] != 0:
            if color == "white":
                act_row, act_col = row, col
            else:
                act_row, act_col = 7 - row, 7 - col

            x = c.board_x + act_col * c.square_length
            y = c.board_y + act_row * c.square_length
            piece = board[row][col]

            if piece == 1:
                piece_image = img.white_pawn
            elif piece == -1:
                piece_image = img.black_pawn
            elif piece == 2:
                piece_image = img.white_knight
            elif piece == -2:
                piece_image = img.black_knight
            elif piece == 3:
                piece_image = img.white_bishop
            elif piece == -3:
                piece_image = img.black_bishop
            elif piece == 4:
                piece_image = img.white_rook
            elif piece == -4:
                piece_image = img.black_rook
            elif piece == 5:
                piece_image = img.white_queen
            elif piece == -5:
                piece_image = img.black_queen
            elif piece == 6:
                piece_image = img.white_king
            elif piece == -6:
                piece_image = img.black_king
            screen.blit(piece_image, (x, y))


def draw_move_coords(move_coords_list, chance, screen):
    if move_coords_list is not None:
        for move_coords in move_coords_list:
            row, col = move_coords

            if chance == "white":
                act_row, act_col = row, col
            else:
                act_row, act_col = 7 - row, 7 - col

            x = c.board_x + (act_col + 0.5) * c.square_length
            y = c.board_y + (act_row + 0.5) * c.square_length
            pg.draw.circle(screen, c.move_color, (x, y), c.move_radius)


def draw_ai_move(moves, screen):
    if moves is not None:
        row, col = moves[0]
        x = c.board_x + col * c.square_length
        y = c.board_y + row * c.square_length
        pg.draw.rect(screen, c.move_color, (x, y, c.square_length, c.square_length), 2)

        row, col = moves[1]
        x = c.board_x + col * c.square_length
        y = c.board_y + row * c.square_length
        pg.draw.rect(screen, c.move_color, (x, y, c.square_length, c.square_length), 2)

def draw_targeted_squares(squares, screen):
    if squares is not None:
        for square in squares:
            x = c.board_x + square[1] * c.square_length
            y = c.board_y + square[0] * c.square_length
            pg.draw.rect(screen, c.targeted_color, (x, y, c.square_length, c.square_length), 4)