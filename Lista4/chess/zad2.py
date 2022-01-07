import chess
import chess.engine
from tqdm import tqdm
import random
import numpy as np
import itertools
from collections import defaultdict
import sys

def analyze(board):
    if board.outcome():
        if board.outcome().winner == chess.WHITE:
            return (1, 0)
        elif board.outcome().winner == chess.BLACK:
            return (0, 1)
        else:
            print("another outcome")
            print(board.outcome())
            return (0, 0)
    info = engine.analyse(
        board, chess.engine.Limit(depth=0)
    )
    score = info["score"].white().score()
    if score == None:
        print(info)
    if score > 0:
        return (1, 0)
    elif score < 0:
        return (0, 1)
    print("score equal zero")
    print(score)
    return (0, 0)

def heuristic(color, board, params):

    if board.outcome():
        if board.outcome().winner == color:
            return 100000
        else:
            return -100000

    wP = len(board.pieces(chess.PAWN, chess.WHITE))
    wK = len(board.pieces(chess.KNIGHT, chess.WHITE))
    wB = len(board.pieces(chess.BISHOP, chess.WHITE))
    wR = len(board.pieces(chess.ROOK, chess.WHITE))
    wQ = len(board.pieces(chess.QUEEN, chess.WHITE))

    bP = len(board.pieces(chess.PAWN, chess.BLACK))
    bK = len(board.pieces(chess.KNIGHT, chess.BLACK))
    bB = len(board.pieces(chess.BISHOP, chess.BLACK))
    bR = len(board.pieces(chess.ROOK, chess.BLACK))
    bQ = len(board.pieces(chess.QUEEN, chess.BLACK))

    turn = board.turn
    board.turn = chess.WHITE
    wM = len(list(board.legal_moves))
    board.turn = chess.BLACK
    bM = len(list(board.legal_moves))
    board.turn = turn

    if color == chess.WHITE:
        val = (
            1.00 * (wP - bP)
            + params[0] * (wK - bK)
            + params[1] * (wB - bB)
            + params[2] * (wR - bR)
            + params[3] * (wQ - bQ)
            + params[4] * (wM - bM)
        )
    else:
        val = (
            1.0 * (bP - wP)
            + params[0] * (bK - wK)
            + params[1] * (bB - wB)
            + params[2] * (bR - wR)
            + params[3] * (bQ - wQ)
            + params[4] * (bM - wM)
        )

    return val

def heuristic_move(board, params):
    moves = list(board.legal_moves)
    max_value = -10000
    best_move = moves[0]
    color = board.turn
    for move in moves:
        board.push(move)
        value = heuristic(color, board, params)
        board.pop()
        if value > max_value:
            max_value = value
            best_move = move
    return best_move

def terminal(board):
    if board.outcome():
        return True
    if board.fullmove_number >= 100:
        return True
    return False

def compare_agents(p1, p2):
    board = chess.Board()
    while not terminal(board):
        if board.turn:
            move = heuristic_move(board, p1)
            board.push(move)
        else:
            move = heuristic_move(board, p2)
            board.push(move)
    result = analyze(board)
    print(board)
    return result

def prepare_pairs():
    for pair in itertools.product(range(100), range(100)):
        if pair[0] != pair[1]:
            yield pair


engine = chess.engine.SimpleEngine.popen_uci(
    "/home/marys/Downloads/stockfish/stockfish_13_linux_x64_bmi2"
)


agents_eval = defaultdict(int)
k = np.random.uniform(low = 1, high = 5, size = (100, 1))
b = np.random.uniform(low = 1, high = 5, size = (100, 1))
r = np.random.uniform(low = 1, high = 8, size = (100, 1))
q = np.random.uniform(low = 1, high = 12, size = (100, 1))
m = np.random.uniform(low = 0, high = 2, size = (100, 1))
agents = np.hstack((k,b,r,q,m))
for pair in prepare_pairs():
    idx1, idx2 = pair
    p1 = agents[idx1]
    p2 = agents[idx2]
    res1, res2 = compare_agents(p1, p2)
    agents_eval[idx1] += res1
    agents_eval[idx2] += res2
    print()
with open('results.txt', 'w') as f:
    for agent_id in sorted(agents_eval, key=agents_eval.get, reverse=True):
        print("Id: "+ str(agent_id) + ", wins: "+ str(agents_eval[agent_id]) + ", params: " + str(agents[agent_id]), file = f)


engine.quit()
