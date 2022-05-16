import pygame as pg

from ai import get_best_move
from constants import consts as c
from images import Images
from moves import get_legal_moves
from render import draw_everything
from utils import *


def game_loop(screen):
    clock = pg.time.Clock()
    img = Images()
    board = init_board()

    player = "white"

    if player == c.chance:
        legal_moves = get_legal_moves(board, c.chance, True)
    else:
        best_move = get_best_move(board, c.chance, c.depth)
        make_move_commons(board, best_move)
        legal_moves = get_legal_moves(board, c.chance, True)
        c.next_turn()

    while True:
        clock.tick(c.fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if inside_board(event.pos):
                    coords = get_click_coords(event.pos)
                    if c.chance == "black":   
                        coords = (7 - coords[0], 7 - coords[1])

                    if c.click_coords is not None:
                        if is_legal_move(coords, c.move_coords_list):
                            make_move_commons(board, [c.click_coords, coords])
                            c.reset_coords()
                            draw_everything(board, img, screen)
                            pg.display.flip()

                            c.next_turn()
                            best_move = get_best_move(board, c.chance, 3)
                            make_move_commons(board, best_move)
                            c.next_turn()
                            legal_moves = get_legal_moves(board, c.chance, True)
                            
                        elif c.click_coords == coords:
                            c.reset_coords()
                        elif clicked_self(board, coords, c.chance):
                            c.click_coords = coords
                            c.move_coords_list = get_move_coords(coords, legal_moves)
                    else:
                        if clicked_self(board, coords, c.chance):
                            if c.click_coords == coords:
                                c.reset_coords()
                            else:
                                c.click_coords = coords
                                c.move_coords_list = get_move_coords(c.click_coords, legal_moves)
                else:
                    c.reset_coords()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        draw_everything(board, img, screen)
        pg.display.flip()


if __name__ == '__main__':
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Chess")
    c.init_screen(screen)

    print("Compiling functions ...")
    game_loop(screen)