import pygame as pg

from constants import consts as c
from load_data import get_resource_path


class Images:
    def __init__(self):
        self.square_area = (c.square_length, c.square_length)

        self.white_pawn = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/white_pawn.png")), self.square_area)
        self.black_pawn = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/black_pawn.png")), self.square_area)
        self.white_rook = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/white_rook.png")), self.square_area)
        self.black_rook = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/black_rook.png")), self.square_area)
        self.white_knight = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/white_knight.png")), self.square_area)
        self.black_knight = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/black_knight.png")), self.square_area)
        self.white_bishop = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/white_bishop.png")), self.square_area)
        self.black_bishop = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/black_bishop.png")), self.square_area)
        self.white_queen = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/white_queen.png")), self.square_area)
        self.black_queen = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/black_queen.png")), self.square_area)
        self.white_king = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/white_king.png")), self.square_area)
        self.black_king = pg.transform.smoothscale(pg.image.load(get_resource_path("pieces/black_king.png")), self.square_area)