import pygame as pg

from constants import consts as c
from game_loop import game_loop

if __name__ == '__main__':
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Chess")
    c.init_screen(screen)
    game_loop(screen)
