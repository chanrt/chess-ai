import pygame as pg

from constants import consts as c
from images import Images
from moves import get_legal_moves
from render import *
from utils import *


def game_loop(screen):
    clock = pg.time.Clock()
    img = Images()
    board = init_board()

    chance = "white"
    click_coords = None
    move_coords_list = None

    legal_moves = get_legal_moves(board, chance, True)

    while True:
        clock.tick(c.fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if inside_board(event.pos):
                    coords = get_click_coords(event.pos)
                    if chance == "black":   
                        coords = (7 - coords[0], 7 - coords[1])

                    if click_coords is not None:
                        if is_legal_move(coords, move_coords_list):
                            board[coords] = board[click_coords]
                            board[click_coords] = 0

                            chance = "white" if chance == "black" else "black"
                            legal_moves = get_legal_moves(board, chance, True)
                            click_coords, move_coords_list = None, None
                        elif click_coords == coords:
                            click_coords, move_coords_list = None, None
                        elif clicked_self(board, coords, chance):
                            click_coords = coords
                            move_coords_list = get_move_coords(coords, legal_moves)
                    else:
                        if clicked_self(board, coords, chance):
                            if click_coords == coords:
                                click_coords, move_coords_list = None, None
                            else:
                                click_coords = coords
                                move_coords_list = get_move_coords(click_coords, legal_moves)
                else:
                    click_coords, move_coords_list = None, None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        screen.fill(c.bg_color)
        draw_background(screen)
        draw_clicked(click_coords, chance, screen)
        draw_board(board, img, chance, screen)
        draw_move_coords(move_coords_list, chance, screen)
        pg.display.flip()


if __name__ == '__main__':
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Chess")
    c.init_screen(screen)
    game_loop(screen)