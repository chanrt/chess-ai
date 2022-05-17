import pygame as pg
from load_data import get_resource_path


class Constants:
    def __init__(self):
        pg.init()

        self.search_depth = 3
        self.chance = "white"
        self.fps = 30
        self.board_fraction = 0.7

        self.click_coords = None
        self.move_coords_list = None

        self.init_colors()
        self.init_sounds()
        self.init_ui()

    def init_colors(self):
        self.bg_color = pg.Color("#003153")
        self.white_color = pg.Color(240, 217, 181)
        self.black_color = pg.Color(181, 136, 99)
        self.selected_color = pg.Color("#3e92cc")
        self.move_color = pg.Color(64, 64, 64)
        self.targeted_color = pg.Color(255, 0, 0)

    def init_sounds(self):
        self.move_sound = pg.mixer.Sound(get_resource_path("sounds/move.mp3"))
        self.capture_sound = pg.mixer.Sound(get_resource_path("sounds/capture.mp3"))
        self.check_sound = pg.mixer.Sound(get_resource_path("sounds/check.wav"))
        self.checkmate_sound = pg.mixer.Sound(get_resource_path("sounds/checkmate.mp3"))
        self.stalemate_sound = pg.mixer.Sound(get_resource_path("sounds/stalemate.wav"))
        self.promote_sound = pg.mixer.Sound(get_resource_path("sounds/promote.wav"))

    def init_bar(self):
        self.progress_x = self.screen_width / 2
        self.progress_length = self.board_length
        self.progress_thickness = int(self.screen_height / 30)

    def init_ui(self):
        self.title_text = None

        self.white_captured_pieces = None
        self.black_captured_pieces = None

        self.restart_button = None
        self.quit_button = None

        self.ai_move = None
        self.targeted_squares = None

    def init_screen(self, screen):
        self.screen_width, self.screen_height = screen.get_size()
        self.board_length = int(self.screen_height * self.board_fraction)
        self.square_length = int(self.board_length / 8)
        self.init_bar()

        self.board_x = int((self.screen_width - self.board_length) / 2)
        self.board_y = int((self.screen_height - self.board_length) / 2)

        self.title_font_size = int(self.screen_height / 10)
        self.button_font_size = int(self.screen_height / 20)

        self.progress_y = self.board_y + self.board_length + (self.screen_height - self.board_length - self.board_y) / 2

        self.button_padding = 10
        self.button_width = int((self.screen_width - self.board_length) / 2) - 4 * self.button_padding
        self.button_height = int(1.5 * self.button_font_size)
        self.button_y = self.board_y + self.board_length + (self.screen_height - self.board_length - self.board_y) / 2
        self.button_def = 2 * (self.board_x - self.screen_width / 4 - self.button_padding)

        self.move_radius = int(self.square_length / 5)

        self.piece_spacing_x = int((self.screen_width - self.board_length) / 6)
        self.piece_spacing_y = int(self.screen_height / 8)

    def next_turn(self):
        if self.chance == "white":
            self.chance = "black"
        else:
            self.chance = "white"

    def reset_coords(self):
        self.click_coords = None
        self.move_coords_list = None


consts = Constants()