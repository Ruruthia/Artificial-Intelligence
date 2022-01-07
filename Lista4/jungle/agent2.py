from collections import defaultdict
import random
from copy import deepcopy
from tqdm import tqdm


class Jungle:
    def __init__(self):
        self.counter = 0
        self.str2idx = {"R": 1, "C": 2, "D": 3, "W": 4, "J": 5, "T": 6, "L": 7, "E": 8}
        self.idx2str = {1: "R", 2: "C", 3: "D", 4: "W", 5: "J", 6: "T", 7: "L", 8: "E"}
        self.board, self.pieces = self.prepare_board()
        self.dens = [(0, 3), (8, 3)]
        self.ponds = {(x, y) for x in [3, 4, 5] for y in [1, 2, 4, 5]}
        self.traps = {(0, 2), (0, 4), (1, 3), (8, 2), (8, 4), (7, 3)}
        self.dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def prepare_board(self):

        board_string = (
            """L.....T.D...C.R.J.W.E.....................e.w.j.r.c...d.t.....l"""
        )
        parsed_board = [board_string[i : i + 7] for i in range(0, len(board_string), 7)]
        board = [7 * [None] for _ in range(9)]
        pieces = defaultdict(dict)
        for i in range(9):
            for j in range(7):
                piece = parsed_board[i][j]
                if piece != ".":
                    if piece.isupper():
                        player = 0
                    else:
                        player = 1
                    board[i][j] = (player, self.str2idx[piece.upper()])
                    pieces[player][self.str2idx[piece.upper()]] = (i, j)
        return board, pieces

    def draw_board(self):
        for i in range(9):
            row = []
            for j in range(7):
                if self.board[i][j] == None:
                    row.append(".")
                else:
                    piece = self.board[i][j]
                    animal = self.idx2str[piece[1]]
                    if piece[0]:
                        animal = animal.lower()
                    row.append(animal)
            print("".join(row))

    def winner(self):
        if self.counter == 30:
            for i in range(8, 0, -1):
                if i in self.pieces[0] and i not in self.pieces[1]:
                    return 0
                if not i in self.pieces[0] and i in self.pieces[1]:
                    return 1
            return 1
        den_0 = self.dens[0]
        den_1 = self.dens[1]
        if self.board[den_0[0]][den_0[1]]:
            return 1
        if self.board[den_1[0]][den_1[1]]:
            return 0
        return -1

    def rat_in_pond(self, player, pos, dx, dy):
        other_player = 1 - player
        n_x = pos[0] + dx
        if 1 not in self.pieces[other_player]:
            return False
        r_x, r_y = self.pieces[other_player][1]
        if (r_x, r_y) not in self.ponds:
            return False
        if dx != 0:
            if pos[1] == r_y:
                return True
        if dy != 0:
            if pos[0] == r_x and abs(pos[1] - r_y) <= 2 and abs(pos[1] + dy - r_y) <= 2:
                return True
        return False

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in self.ponds and pos2 in self.ponds:
            return True
        if pos1 in self.ponds:
            return False
        if p1 == 1 and p2 == 8:
            return True
        if p1 == 8 and p2 == 1:
            return False
        if p1 >= p2:
            return True
        if p2 in self.traps:
            return True
        return False

    def possible_moves(self, player):
        moves = []
        for p, pos in self.pieces[player].items():
            for dir in self.dirs:
                dx, dy = dir
                new_pos = (pos[0] + dx, pos[1] + dy)
                if 0 <= new_pos[0] < 9 and 0 <= new_pos[1] < 7:
                    if self.dens[player] == new_pos:
                        continue
                    if new_pos in self.ponds:
                        if p not in [1, 6, 7]:
                            continue
                        if p == 6 or p == 7:
                            if dx != 0:
                                dx *= 4
                            if dy != 0:
                                dy *= 3
                            if self.rat_in_pond(player, pos, dx, dy):
                                continue
                        new_pos = (pos[0] + dx, pos[1] + dy)
                    nx, ny = new_pos
                    if self.board[nx][ny] is not None:
                        pl, piece = self.board[nx][ny]
                        if pl == player:
                            continue
                        if not self.can_beat(p, piece, pos, new_pos):
                            continue
                    moves.append((pos, new_pos))
        return moves

    def do_move(self, player, move):
        if move is None:
            return
        pos1, pos2 = move
        x, y = pos1
        pl, pc = self.board[x][y]

        x2, y2 = pos2
        if self.board[x2][y2]:
            pl2, pc2 = self.board[x2][y2]
            del self.pieces[pl2][pc2]
            self.counter = 0
        else:
            self.counter += 1

        self.pieces[pl][pc] = (x2, y2)
        self.board[x2][y2] = (pl, pc)
        self.board[x][y] = None

    def random_move(self, player):
        ms = self.possible_moves(player)
        if ms:
            return random.choice(ms)
        return None

    def copy(self):
        return deepcopy(self)

    def simulated_move(self, player, K):
        ms = self.possible_moves(player)
        if not ms:
            return None
        moves_dict = defaultdict(int)
        while K > 0:
            for idx in range(len(ms)):
                move = ms[idx]
                game = deepcopy(self)
                game.counter = 0
                result, movecount = game.simulate_game(move, player)
                moves_dict[idx] += result
                K -= movecount
                if K < 0:
                    break
        best_move_idx = max(moves_dict, key=moves_dict.get)
        return ms[best_move_idx]

    def simulate_game(self, move, player):
        move_count = 1
        self.do_move(player, move)
        curr_player = 1 - player
        while self.winner() == -1:
            move_count += 1
            move = self.random_move(curr_player)
            self.do_move(curr_player, move)
            curr_player = 1 - curr_player
        if self.winner() == player:
            return 1, move_count
        else:
            return -1, move_count

    def heuristic(self):
        W = [2, 2, 3, 4, 5, 8, 9, 10]
        p1_animals = 0
        p0_animals = 0
        p1_toden = 1000
        p0_toden = 1000
        for i in range(1, 9):
            if i in self.pieces[1]:
                p1_animals += W[i - 1]
                toden_m = abs(self.pieces[1][i][0] - self.dens[0][0]) + abs(
                    self.pieces[1][i][1] - self.dens[0][1]
                )

                if toden_m < p1_toden:
                    p1_toden = toden_m

            if i in self.pieces[0]:
                p0_animals += W[i - 1]
                toden_m = abs(self.pieces[0][i][0] - self.dens[1][0]) + abs(
                    self.pieces[0][i][1] - self.dens[1][1]
                )

                if toden_m < p0_toden:
                    p0_toden = toden_m
        a = p1_animals - p0_animals

        m = len(self.possible_moves(1)) - len(self.possible_moves(0))
        d = p0_toden - p1_toden
        return 5 * a + m + 2 * d

    def minimax_move(self, player, depth, alpha, beta):
        best_move = None
        if depth == 0 or self.winner() != -1:
            v = self.heuristic()
            return v, best_move
        ms = self.possible_moves(player)
        if len(ms) == 0:
            v = self.heuristic()
            return v, best_move
        if player:
            value = -100000
            for move in ms:
                game = deepcopy(self)
                game.do_move(player, move)
                new_value, _ = game.minimax_move(1 - player, depth - 1, alpha, beta)
                if new_value > value:
                    value = new_value
                    best_move = move
                if value >= beta:
                    return value, best_move
                alpha = max(alpha, value)
            return value, best_move
        else:
            value = 100000
            for move in ms:
                game = deepcopy(self)
                game.do_move(player, move)
                new_value, _ = game.minimax_move(1 - player, depth - 1, alpha, beta)

                if new_value < value:
                    value = new_value
                    best_move = move
                if value <= alpha:
                    return value, best_move
                beta = min(beta, value)
            return value, best_move


wins = 0
for _ in tqdm(range(10)):
    j = Jungle()
    our_position = random.choice([0, 1])
    current_player = 0
    while j.winner() == -1:
        if current_player == our_position:
            v, move = j.minimax_move(current_player, 2, -20000, 20000)
        else:
            move = j.simulated_move(current_player, 20000)
        j.do_move(current_player, move)
        current_player = 1 - current_player
    j.draw_board()
    print(len(j.pieces[0]))
    print(len(j.pieces[1]))
    if j.winner() == our_position:
        wins += 1
    print(wins)
print(wins)
