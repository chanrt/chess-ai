import pygame as pg

class ProgressBar:
    def __init__(self, x, y, length, thickness, screen):
        self.x = x
        self.y = y
        self.length = length
        self.thickness = thickness
        self.screen = screen

        # display state
        self.display = True

        # orientation
        self.orientation = "horizontal"

        # progress variable (between 0 and 1)
        self.progress = 0

        # border properties
        self.border_color = pg.Color("white")
        self.border_width = 2

        # color properties
        self.bg_color = pg.Color("gray")
        self.fg_color = pg.Color("red")

        self.make_rects()

    def set_horizontal(self):
        self.orientation = "horizontal"
        self.make_rects()

    def set_vertical(self):
        self.orientation = "vertical"
        self.make_rects()

    def increase_progress(self, amount):
        self.progress += amount
        self.normalize()
        self.make_rects()

    def set_progress(self, progress):
        self.progress = progress
        self.normalize()
        self.make_rects()

    def normalize(self):
        if self.progress > 1:
            self.progress = 1
        elif self.progress < 0:
            self.progress = 0

    def make_rects(self):
        if self.orientation == "horizontal":
            self.bg_rect = pg.Rect(self.x - self.length // 2, self.y - self.thickness // 2, self.length, self.thickness)
            self.fg_rect = pg.Rect(self.x - self.length // 2, self.y - self.thickness // 2, self.length * self.progress, self.thickness)
        else:
            self.bg_rect = pg.Rect(self.x - self.thickness // 2, self.y - self.length // 2, self.thickness, self.length)
            self.fg_rect = pg.Rect(self.x - self.thickness // 2, self.y - self.length // 2 + self.length * (1 - self.progress), self.thickness, self.length * self.progress)

    def render(self):
        if self.display:
            pg.draw.rect(self.screen, self.bg_color, self.bg_rect)
            pg.draw.rect(self.screen, self.fg_color, self.fg_rect)
            pg.draw.rect(self.screen, self.border_color, self.bg_rect, self.border_width)