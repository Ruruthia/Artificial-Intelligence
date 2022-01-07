import random
import chess
from tqdm import tqdm


def scholars_mate(moves, board):
    if len(moves) == 0:
        return False
    else:
        move = moves.pop(0)
        try:
            m = board.parse_san(move)
            board.push_san(move)
            return True
        except:
            return False


def random_move(board):
    moves = list(board.legal_moves)
    if len(moves) == 0:
        return True
    move = random.choice(moves)
    board.push(move)
    return False


def minimax_move(board, depth, alpha, beta):
    best_move = None
    if depth == 0 or terminal(board):
        return eval(board), best_move
    moves = board.legal_moves
    if not board.legal_moves.count():
        return eval(board), best_move
    if board.turn == chess.WHITE:
        value = -10000000
        for move in moves:
            board.push(move)
            new_value, _ = minimax_move(board, depth - 1, alpha, beta)
            board.pop()
            if new_value > value:
                value = new_value
                best_move = move
            if value >= beta:
                return value, best_move
            alpha = max(alpha, value)
        return value, best_move
    else:
        value = 10000000
        for move in moves:
            board.push(move)
            new_value, _ = minimax_move(board, depth - 1, alpha, beta)
            board.pop()
            if new_value < value:
                value = new_value
                best_move = move
            if value <= alpha:
                return value, best_move
            beta = min(beta, value)
        return value, best_move


def eval(board):
    if board.outcome():
        if board.outcome().winner:
            return 100000
        else:
            return -100000
    val = 0

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

    val = (
        10 * (wP - bP)
        + 30 * (wK - bK)
        + 30 * (wB - bB)
        + 50 * (wR - bR)
        + 90 * (wQ - bQ)
        + 10 * (wM - bM)
    )
    return val


def terminal(board):
    if board.outcome():
        return True
    if board.fullmove_number >= 100:
        return True
    return False


def play_one_game():
    board = chess.Board()
    opening = ["e4", "Qh5", "Bc4", "Qxf7#"]
    sm_possible = True
    while not terminal(board):
        if board.turn == chess.WHITE:
            if sm_possible:
                sm_possible = scholars_mate(opening, board)
            else:
                val, move = minimax_move(board, 2, -10000000, 10000000)
                board.push(move)
        else:
            draw = random_move(board)
            if draw:
                return 0
    if board.fullmove_number == 100:
        return -100
    if board.outcome().winner:
        return 100 - board.fullmove_number
    else:
        return -1000


result = 0
scholar_mates = 0
for _ in tqdm(range(50)):
    val = play_one_game()
    if val == 96:
        scholar_mates += 1
    result += val
print(result)
print(scholar_mates)
