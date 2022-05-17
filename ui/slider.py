import pygame as pg


class Slider:

    def __init__(self, x, y, length, thickness, screen):
        self.x = x
        self.y = y
        self.length = length
        self.thickness = thickness

        self.screen = screen

        # more geometric properties
        self.hook_radius = thickness // 4
        self.border_width = length // 20
        self.actual_length = self.length - 2 * self.border_width
        self.slider_thickness = thickness // 10
        self.start_x = self.x - self.length // 2 + self.border_width
        self.end_x = self.x + self.length // 2 - self.border_width

        self.display = True

        self.value = 0.5
        self.update_hook_position()

        self.bg_color = "black"
        self.slider_color = "white"
        self.hook_color = "gray"

        self.make_rects()

    def inside_rect(self, pos):
        mouse_x, mouse_y = pos
        if (self.x - self.length // 2 < mouse_x < self.x + self.length // 2) and (self.y - self.thickness // 2 < mouse_y < self.y + self.thickness // 2):
            return True
        else:
            return False

    def check_clicked(self, pos):
        if self.inside_rect(pos):
            mouse_x, _ = pos
            if self.x < mouse_x < self.start_x:
                self.value = 0
            elif self.end_x < mouse_x < self.x + self.length // 2:
                self.value = 1
            else:
                self.value = (mouse_x - self.start_x) / self.actual_length
            self.update_hook_position()

    def make_rects(self):
        self.outer_rect = pg.Rect(self.x - self.length // 2,
                                  self.y - self.thickness // 2, self.length,
                                  self.thickness)
        self.slider_rect = pg.Rect(
            self.x - self.length // 2 + self.border_width,
            self.y - self.slider_thickness // 2,
            self.length - 2 * self.border_width, self.slider_thickness)

    def update_hook_position(self):
        self.hook_position = self.start_x + self.value * self.actual_length

    def render(self):
        if self.display:
            pg.draw.rect(self.screen, self.bg_color, self.outer_rect)
            pg.draw.rect(self.screen, self.slider_color, self.slider_rect)
            pg.draw.circle(
                self.screen, self.hook_color,
                (self.hook_position, self.y),
                self.hook_radius)
