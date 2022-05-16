from numba import njit
import numpy as np

from moves import get_legal_moves, make_move
from evaluator import evaluate
from utils import *


def minimax(board, color, depth):
    if depth == 0:
        return evaluate(board)

    nodes = []
    legal_moves = get_legal_moves(board, color, True)

    for move in legal_moves:
        temp_board = np.copy(board)
        make_move_commons(temp_board, move)
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


def get_best_move(board, color, depth):
    branches = []
    legal_moves = get_legal_moves(board, color, True)

    for move in legal_moves:
        temp_board = np.copy(board)
        make_move_commons(temp_board, move)
        branches.append(temp_board)

    enemy_color = "white" if color == "black" else "black"
    evaluations = []

    for i, branch in enumerate(branches):
        print(f"Move #{i + 1} of {len(branches)}")
        evaluation = minimax(branch, enemy_color, depth - 1)
        print(branch)
        print(f"Evaluation: {evaluation}\n")
        evaluations.append(evaluation)
    
    if color == "white":
        best_eval = max(evaluations)
    else:
        best_eval = min(evaluations)

    best_eval_index = evaluations.index(best_eval)

    print(f"Played move #{best_eval_index + 1}")
    print(branches[best_eval_index])
    print(f"With evaluation: {best_eval} at search depth: {depth}\n")
    print("=" * 20)

    return legal_moves[best_eval_index]