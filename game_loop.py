import numpy as np
import pygame as pg

from ai import get_best_move
from constants import consts as c
from images import Images
from load_data import get_resource_path
from moves import get_legal_moves
from progress_bar import ProgressBar
from render import draw_everything
from sound_handler import *
from utils import *


def game_loop(screen):
    clock = pg.time.Clock()
    img = Images()
    board = init_board()
    board_record = [np.copy(board)]

    player = "white"
    progress_bar = ProgressBar(c.progress_x, c.progress_y, c.progress_length, c.progress_thickness, screen)

    pg.mixer.music.load(get_resource_path("sounds/bg_music.mp3"))
    pg.mixer.music.set_volume(0.5)
    music_started = False

    if player == c.chance:
        legal_moves = get_legal_moves(board, c.chance, True)
    else:
        best_move = get_best_move(board, c.chance, c.depth)
        make_move_commons(board, best_move)
        c.move_sound.play()
        board_record.append(np.copy(board))
        c.next_turn()
        legal_moves = get_legal_moves(board, c.chance, True)

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
                            # Finish player's turn
                            play_move_sound(board, coords)
                            make_move_commons(board, [c.click_coords, coords])
                            board_record.append(np.copy(board))
                            c.reset_coords()
                            draw_everything(board, img, screen)
                            pg.display.flip()

                            if is_enemy_in_check(board, player):
                                play_check_sound()

                            # Start AI turn
                            c.next_turn()
                            best_move = get_best_move(board, c.chance, c.search_depth, progress_bar)

                            if best_move is None:
                                if is_enemy_in_check(board, player):
                                    play_checkmate_sound()
                                    exit_game()
                                else:
                                    play_stalemate_sound()
                                    exit_game()
                            else:
                                play_move_sound(board, best_move[1])
                                make_move_commons(board, best_move)
                                board_record.append(np.copy(board))
                                c.next_turn()
                                legal_moves = get_legal_moves(board, c.chance, True)

                                if is_player_in_check(board, player):
                                    play_check_sound()
                                elif len(legal_moves) == 0:
                                    if is_player_in_check(board, player):
                                        play_checkmate_sound()
                                        exit_game()
                                    else:
                                        play_stalemate_sound()
                                        exit_game()
                            
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

                if event.key == pg.K_r:
                    board = init_board()
                    board_record = [np.copy(board)]
                    c.chance = "white"
                    c.reset_coords()
                    pg.mixer.music.rewind()

                    if player == c.chance:
                        legal_moves = get_legal_moves(board, c.chance, True)
                    else:
                        best_move = get_best_move(board, c.chance, c.depth, progress_bar)
                        make_move_commons(board, best_move)
                        board_record.append(np.copy(board))
                        c.next_turn()
                        legal_moves = get_legal_moves(board, c.chance, True)
                
                if event.key == pg.K_u:
                    if len(board_record) > 2:
                        board_record.pop()
                        board_record.pop()
                        board = board_record.pop()
                        c.reset_coords()
                        legal_moves = get_legal_moves(board, c.chance, True)


        draw_everything(board, img, screen)
        pg.display.flip()

        if not music_started:
            pg.mixer.music.play()
            music_started = True


def exit_game():
    pg.time.delay(3000)
    pg.quit()
    quit()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Chess")
    c.init_screen(screen)

    print("Compiling functions ...")
    game_loop(screen)