import numpy as np
import pygame as pg

from ai import get_best_move
from ui.button import Button
from ui.captured_piece import CapturedPieceManager
from constants import consts as c
from images import Images
from load_data import get_resource_path
from moves import get_legal_moves
from ui.progress_bar import ProgressBar
from render import draw_everything
from ui.sound_handler import *
from ui.text import Text
from utils import *


def game_loop(screen, player = "white"):
    c.chance = "white"

    clock = pg.time.Clock()
    img = Images()
    board = init_board()
    board_record = [np.copy(board)]

    c.white_captured_pieces = CapturedPieceManager(img, "white", screen)
    c.black_captured_pieces = CapturedPieceManager(img, "black", screen)

    title_font = pg.font.Font(get_resource_path("fonts/macondo.ttf"), c.title_font_size)
    button_font = pg.font.Font(get_resource_path("fonts/macondo.ttf"), c.button_font_size)

    c.title_text = Text(c.screen_width / 2, c.screen_height / 15, "Chess AI", screen)
    c.title_text.set_font(title_font)

    c.restart_button = Button(c.screen_width / 4 - c.button_def, c.button_y, c.button_width, c.button_height, screen, "Restart")
    c.restart_button.set_font(button_font)

    c.quit_button = Button(3 * c.screen_width / 4 + c.button_def, c.button_y, c.button_width, c.button_height, screen, "Quit")
    c.quit_button.set_font(button_font)

    progress_bar = ProgressBar(c.progress_x, c.progress_y, c.progress_length, c.progress_thickness, screen)

    pg.mixer.music.load(get_resource_path("sounds/bg_music.mp3"))
    pg.mixer.music.set_volume(0.5)
    music_started = False

    c.ai_move = None
    c.targeted_squares = None

    if player == c.chance:
        legal_moves = get_legal_moves(board, c.chance, True)
    else:
        best_move = get_best_move(board, c.chance, c.search_depth, progress_bar)
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

            if event.type == pg.MOUSEMOTION:
                mouse_pos = pg.mouse.get_pos()

                c.restart_button.update(mouse_pos)
                c.quit_button.update(mouse_pos)

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                clicks = event.button

                c.restart_button.check_clicked(mouse_pos, clicks)
                c.quit_button.check_clicked(mouse_pos, clicks)

                if c.restart_button.left_clicked:
                    # restart game
                    board = init_board()
                    board_record = [np.copy(board)]

                    c.chance = "white"
                    c.reset_coords()
                    c.ai_move = None
                    c.targeted_squares = None
                    c.white_captured_pieces.get_captured_pieces(board)
                    c.black_captured_pieces.get_captured_pieces(board)

                    pg.mixer.music.rewind()

                    if player == c.chance:
                        legal_moves = get_legal_moves(board, c.chance, True)
                    else:
                        best_move = get_best_move(board, c.chance, c.search_depth, progress_bar)
                        make_move_commons(board, best_move)
                        board_record.append(np.copy(board))
                        c.next_turn()
                        legal_moves = get_legal_moves(board, c.chance, True)

                if c.quit_button.left_clicked:
                    pg.mixer.music.stop()
                    return

                if inside_board(event.pos):
                    coords = get_click_coords(event.pos)

                    if c.chance == "black":   
                        coords = (7 - coords[0], 7 - coords[1])

                    if c.click_coords is not None:
                        if is_legal_move(coords, c.move_coords_list):
                            # Finish player's turn
                            play_move_sound(board, coords)
                            make_move_commons(board, [c.click_coords, coords])
                            check_promotions(board)
                        
                            castling_status = is_castling_move(board, [c.click_coords, coords], player)
                            if castling_status is not None:
                                row = 7 if player == "white" else 0
                                if castling_status == 1:
                                    # kingside castling
                                    make_move_commons(board, [(row, 7), (row, 5)])
                                elif castling_status == 2:
                                    # queenside castling
                                    make_move_commons(board, [(row, 0), (row, 3)])

                            c.white_captured_pieces.get_captured_pieces(board)
                            c.black_captured_pieces.get_captured_pieces(board)
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
                                # Finish AI turn
                                c.ai_move = best_move
                                play_move_sound(board, best_move[1])
                                make_move_commons(board, best_move)
                                check_promotions(board)
                                c.targeted_squares = get_targeted_squares(board, player)

                                c.white_captured_pieces.get_captured_pieces(board)
                                c.black_captured_pieces.get_captured_pieces(board)
                                board_record.append(np.copy(board))

                                # Start player turn
                                c.next_turn()
                                legal_moves = get_legal_moves(board, c.chance, True)
                                castling_moves = check_castling(board, board_record, player)

                                if len(castling_moves) != 0:
                                    legal_moves.extend(castling_moves)

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

            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                clicks = event.button

                c.restart_button.check_released(mouse_pos, clicks)
                c.quit_button.check_released(mouse_pos, clicks)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

                if event.key == pg.K_r:
                    board = init_board()
                    board_record = [np.copy(board)]

                    c.ai_move = None
                    c.chance = "white"
                    c.reset_coords()
                    c.white_captured_pieces.get_captured_pieces(board)
                    c.black_captured_pieces.get_captured_pieces(board)
                    c.targeted_squares = None

                    pg.mixer.music.rewind()

                    if player == c.chance:
                        legal_moves = get_legal_moves(board, c.chance, True)
                    else:
                        best_move = get_best_move(board, c.chance, c.search_depth, progress_bar)
                        make_move_commons(board, best_move)
                        board_record.append(np.copy(board))
                        c.next_turn()
                        legal_moves = get_legal_moves(board, c.chance, True)
                
                if event.key == pg.K_u:
                    if len(board_record) > 2:
                        board_record.pop()
                        board_record.pop()
                        board = np.copy(board_record[-1])
                        c.ai_move = None
                        c.white_captured_pieces.get_captured_pieces(board)
                        c.black_captured_pieces.get_captured_pieces(board)
                        c.reset_coords()
                        legal_moves = get_legal_moves(board, c.chance, True)


        draw_everything(board, img, screen)
        pg.display.flip()

        if not music_started:
            pg.mixer.music.play(-1)
            music_started = True


def exit_game():
    pg.mixer.music.stop()
    pg.time.delay(3000)
    return


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    pg.display.set_caption("Chess AI")
    c.init_screen(screen)

    print("Compiling functions ...")
    game_loop(screen)