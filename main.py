from math import ceil
import pygame as pg

from ui.button import Button
from constants import consts as c
from game_loop import game_loop
from load_data import get_resource_path
from ui.slider import Slider
from ui.text import Text


def main_menu(screen):
    bg_image = pg.image.load(get_resource_path("images/background.jpg"))
    bg_image = pg.transform.smoothscale(bg_image, screen.get_size())

    title_font = pg.font.Font(get_resource_path('fonts/macondo.ttf'), c.title_font_size)
    button_font = pg.font.Font(get_resource_path('fonts/macondo.ttf'), c.button_font_size)

    title_text = Text(c.screen_width / 2, c.title_font_size, "Chess AI", screen)
    title_text.set_font(title_font)

    about_text = Text(c.screen_width / 2, 2 * c.title_font_size, "Developed by ChanRT | Fork me at GitHub", screen)
    about_text.set_font(button_font)

    white_button = Button(c.screen_width / 4, c.screen_height / 2, c.button_width, c.button_height, screen, "Play as white")
    white_button.set_font(button_font)

    black_button = Button(3 * c.screen_width / 4, c.screen_height / 2, c.button_width, c.button_height, screen, "Play as black")
    black_button.set_font(button_font)

    depth_slider = Slider(c.screen_width / 2, 3 * c.screen_height / 4, c.screen_width / 5, 50, screen)

    depth_text = Text(c.screen_width / 2, 3 * c.screen_height / 4 + 50, "Search depth: " + str(get_search_depth(depth_slider)), screen)
    depth_text.set_font(button_font)

    exit_button = Button(c.screen_width - 150, c.screen_height - 75, 150, 75, screen, "Exit")
    exit_button.set_font(button_font)

    please_wait_text = Text(c.screen_width / 2, c.screen_height - c.button_font_size, "Compiling functions, please wait ...", screen)
    please_wait_text.set_font(button_font)
    please_wait_text.display = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            if event.type == pg.MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()

                white_button.update(mouse_pos)
                black_button.update(mouse_pos)
                exit_button.update(mouse_pos)

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                clicks = event.button

                white_button.check_clicked(mouse_pos, clicks)
                black_button.check_clicked(mouse_pos, clicks)
                depth_slider.check_clicked(mouse_pos)
                exit_button.check_clicked(mouse_pos, clicks)

                depth_text.set_text("Search depth: " + str(get_search_depth(depth_slider)))

                if white_button.left_clicked or black_button.left_clicked:
                    c.search_depth = get_search_depth(depth_slider)
                    please_wait_text.display = True
                    please_wait_text.render()
                    pg.display.flip()

                    if white_button.left_clicked:
                        game_loop(screen, "white")
                        white_button.left_clicked = False
                    elif black_button.left_clicked:
                        game_loop(screen, "black")
                        black_button.left_clicked = False
                    please_wait_text.display = False
                if exit_button.left_clicked:
                    pg.quit()
                    quit()

            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                clicks = event.button

                white_button.check_released(mouse_pos, clicks)
                black_button.check_released(mouse_pos, clicks)
                exit_button.check_released(mouse_pos, clicks)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        screen.blit(bg_image, (0, 0))
        title_text.render()
        about_text.render()
        white_button.render()
        black_button.render()
        depth_slider.render()
        depth_text.render()
        exit_button.render()

        pg.display.flip()


def get_search_depth(slider):
    depth = ceil(slider.value / 0.2)
    if depth == 0:
        return 1
    else:
        return depth

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("Chess AI")
    c.init_screen(screen)
    main_menu(screen)
