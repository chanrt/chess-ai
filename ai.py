import numpy as np
import pygame as pg

from moves import get_legal_moves
from evaluator import evaluate
from utils import *


def minimax(board, color, depth):
    if depth == 0:
        return evaluate(board)

    nodes = []
    legal_moves = get_legal_moves(board, color, True)

    if len(legal_moves) == 0:
        return evaluate(board)

    for move in legal_moves:
        temp_board = np.copy(board)
        temp_board[move[1]] = temp_board[move[0]]
        temp_board[move[0]] = 0
        nodes.append(temp_board)

    enemy_color = "white" if color == "black" else "black"
    evaluations = []

    for node in nodes:
        evaluations.append(minimax(node, enemy_color, depth - 1))

    if color == "white":
        best_eval = max(evaluations)
    else:
        best_eval = min(evaluations)

    return best_eval


def get_best_move(board, color, depth, progress_bar):
    branches = []
    legal_moves = get_legal_moves(board, color, True)

    if len(legal_moves) == 0:
        return None

    for move in legal_moves:
        temp_board = np.copy(board)
        make_move_commons(temp_board, move)
        branches.append(temp_board)

    enemy_color = "white" if color == "black" else "black"
    evaluations = []

    for i, branch in enumerate(branches):
        evaluation = minimax(branch, enemy_color, depth - 1)
        progress_bar.set_progress((i + 1) / len(branches))
        progress_bar.render()
        pg.display.flip()

        print(f"Move #{i + 1} of {len(branches)}")
        print(branch)
        print(f"Evaluation: {evaluation}\n")
        evaluations.append(evaluation)
    
    if color == "white":
        best_eval = max(evaluations)
    else:
        best_eval = min(evaluations)

    best_eval_index = evaluations.index(best_eval)

    print(f"Best move #{best_eval_index + 1}")
    print(branches[best_eval_index])
    print(f"With evaluation: {best_eval} at search depth: {depth}\n")
    print("=" * 20)

    return legal_moves[best_eval_index]