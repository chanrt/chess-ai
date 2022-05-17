from constants import consts as c


def play_move_sound(board, final_pos):
    if board[final_pos] == 0:
        c.move_sound.play()
    else:
        c.capture_sound.play()

def play_check_sound():
    c.check_sound.play()

def play_stalemate_sound():
    c.stalemate_sound.play()

def play_checkmate_sound():
    c.checkmate_sound.play()