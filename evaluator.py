from numba import njit


@njit(nogil=True)
def in_center(row, col):
    return 2 < row < 5 and 2 < col < 5


@njit(nogil=True)
def evaluate(board):
    white_score = 0
    black_score = 0

    for row in range(8):
        for col in range(8):
            if board[row][col] == 1:
                white_score += 1
                if 2 < row < 5 and 2 < col < 5:
                    white_score += 0.5
            elif board[row][col] == 2 or board[row][col] == 3:
                white_score += 3
                if 2 < row < 5 and 2 < col < 5:
                    white_score += 1
            elif board[row][col] == 4:
                white_score += 5
                if 2 < row < 5 and 2 < col < 5:
                    white_score += 2
            elif board[row][col] == 5:
                white_score += 9
                if 2 < row < 5 and 2 < col < 5:
                    white_score += 3
            elif board[row][col] == -1:
                black_score += 0.5
                if 2 < row < 5 and 2 < col < 5:
                    black_score += 1
            elif board[row][col] == -2 or board[row][col] == -3:
                black_score += 3
                if 2 < row < 5 and 2 < col < 5:
                    black_score += 1
            elif board[row][col] == -4:
                black_score += 5
                if 2 < row < 5 and 2 < col < 5:
                    black_score += 2
            elif board[row][col] == -5:
                black_score += 9
                if 2 < row < 5 and 2 < col < 5:
                    black_score += 3
    
    return white_score - black_score