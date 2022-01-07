import random
from copy import deepcopy
import time
from tqdm import tqdm
import numpy as np

M = 8


class Reversi:

    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = self.initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(M):
            for j in range(M):
                if self.board[i][j] is None:
                    self.fields.add((i, j))

    def initial_board(self):
        B = [[None] * M for _ in range(M)]
        B[3][3] = 1
        B[4][4] = 1
        B[3][4] = 0
        B[4][3] = 0
        return B

    def get(self, x, y):
        if 0 <= x < M and 0 <= y < M:
            return self.board[x][y]
        return None

    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player) for direction in self.DIRS):
                res.append((x, y))
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def draw(self):
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                if b is None:
                    res.append(".")
                elif b == 1:
                    res.append("#")
                else:
                    res.append("o")
            print("".join(res))
        print("")

    def result(self):
        res = 0
        for x in range(M):
            for y in range(M):
                b = self.board[x][y]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)
        if move is None:
            return
        x, y = move
        x0, y0 = move
        self.board[x][y] = player
        self.fields -= set([move])
        for dx, dy in self.DIRS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[nx][ny] = player

    def reverse_move(self):
        h = self.history.pop(-1)
        self.board = h
        s = set([self.move_list.pop(-1)])
        self.fields = self.fields | s


class Game:
    def __init__(self):
        self.our_position = random.choice([0, 1])
        self.player = 1
        self.reversi = Reversi()

    def heuristic(self, board):

        player = 1

        board_arr = board.board
        p_m = len(board.moves(player))
        o_m = len(board.moves(1 - player))

        o_c, p_c = 0, 0
        for a in [0, M - 1]:
            for b in [0, M - 1]:
                if board_arr[a][b] == 1:
                    p_c += 1
                elif board_arr[a][b] == 0:
                    o_c += 1

        c = 25 * (p_c - o_c)

        p_cp, o_cp = 0, 0
        if board_arr[0][0] == None:
            c1_p = np.array([board_arr[0][1], board_arr[1][0], board_arr[1][1]])
            p_cp += np.sum(c1_p == player)
            o_cp += np.sum(c1_p == (1 - player))
        if board_arr[M - 1][M - 1] == None:
            c2_p = np.array(
                [
                    board_arr[M - 1][M - 2],
                    board_arr[M - 2][M - 1],
                    board_arr[M - 2][M - 2],
                ]
            )
            p_cp += np.sum(c2_p == player)
            o_cp += np.sum(c2_p == (1 - player))
        if board_arr[0][M - 1] == None:
            c3_p = np.array(
                [board_arr[1][M - 1], board_arr[0][M - 2], board_arr[1][M - 2]]
            )
            p_cp += np.sum(c3_p == player)
            o_cp += np.sum(c3_p == (1 - player))
        if board_arr[M - 1][0] == None:
            c4_p = np.array(
                [board_arr[M - 1][1], board_arr[M - 2][0], board_arr[M - 2][1]]
            )
            p_cp += np.sum(c4_p == player)
            o_cp += np.sum(c4_p == (1 - player))

        cp = -12.5 * (p_cp - o_cp)

        if p_m > o_m:
            m = (100 * p_m) / (p_m + o_m)
        elif p_m < o_m:
            m = -(100 * o_m) / (p_m + o_m)
        else:
            m = 0

        v = 800 * c + 380 * cp + 80 * m
        return v

    def minimax_move(self, player, depth, board, alpha, beta):

        best_move = None
        if depth == 0 or board.terminal():
            v = self.heuristic(board)
            return v, best_move
        ms = board.moves(player)
        if len(board.moves(player)) == 0:
            v = self.heuristic(board)
            return v, best_move
        if player:
            value = -10000000
            for move in ms:
                board.do_move(move, player)
                new_value, _ = self.minimax_move(
                    1 - player, depth - 1, board, alpha, beta
                )
                board.reverse_move()
                if new_value > value:
                    value = new_value
                    best_move = move
                if value >= beta:
                    return value, best_move
                alpha = max(alpha, value)
            return value, best_move
        else:
            value = 10000000
            for move in ms:
                board.do_move(move, player)
                new_value, _ = self.minimax_move(
                    1 - player, depth - 1, board, alpha, beta
                )
                board.reverse_move()
                if new_value < value:
                    value = new_value
                    best_move = move
                if value <= alpha:
                    return value, best_move
                beta = min(beta, value)
            return value, best_move

    def play(self):
        while not self.reversi.terminal():

            if self.player == self.our_position:
                val, move = self.minimax_move(
                    self.player, 2, self.reversi, -10000000, 10000000
                )
            else:
                move = self.reversi.random_move(self.player)
            self.reversi.do_move(move, self.player)
            self.player = 1 - self.player

        if self.our_position:
            return self.reversi.result() > 0
        else:
            return self.reversi.result() < 0


wins = 0
start = time.time()
for i in tqdm(range(1000)):
    g = Game()
    if g.play():
        wins += 1
end = time.time()
print(wins)
print(end - start)
