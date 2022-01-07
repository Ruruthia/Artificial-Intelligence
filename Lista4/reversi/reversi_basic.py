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
        self.player = 1
        self.move_list = []
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

    def moves(self):
        player = self.player
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

    def random_move(self):
        ms = self.moves()
        if ms:
            return random.choice(ms)
        return None

    def do_move(self, move):
        self.move_list.append(move)
        player = self.player
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
        self.player = 1 - player

    def copy(self):
        return deepcopy(self)
