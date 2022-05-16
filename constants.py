import pygame as pg


class Constants:
    def __init__(self):
        self.fps = 30
        self.board_fraction = 0.7

        self.init_colors()

    def init_colors(self):
        self.bg_color = pg.Color(32, 32, 32)
        self.white_color = pg.Color(240, 217, 181)
        self.black_color = pg.Color(181, 136, 99)
        self.selected_color = pg.Color("#3e92cc")
        self.move_color = pg.Color("red")

    def init_screen(self, screen):
        self.screen_width, self.screen_height = screen.get_size()
        self.board_length = int(self.screen_height * self.board_fraction)
        self.square_length = int(self.board_length / 8)

        self.board_x = int((self.screen_width - self.board_length) / 2)
        self.board_y = int((self.screen_height - self.board_length) / 2)

        self.move_radius = int(self.square_length / 6)


consts = Constants()