from reversi_basic import *
from math import sqrt, log
from tqdm import tqdm


class Node:
    def __init__(self, game=None, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.move = None
        self.games = 0.0
        self.wins = 0.0
        self.untried_moves = []
        if game:
            self.untried_moves = game.moves()

    def ucb(self):
        return (self.wins / self.games) + sqrt(
            2.0 * log(self.parent.games) / self.games
        )

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.game.terminal() or (
            len(self.children) == 0 and len(self.untried_moves) == 0
        )

    def expand(self):
        move = self.untried_moves.pop(0)
        new_game = self.game.copy()
        new_game.do_move(move)
        child = Node(new_game, self)
        self.children.append(child)
        child.move = move
        return child

    def rollout(self, player):
        new_game = self.game.copy()
        # print(player)
        while not new_game.terminal():
            move = new_game.random_move()
            new_game.do_move(move)
        if new_game.result() > 0:
            if player:
                return 1
            else:
                return 0
        elif new_game.result() < 0:
            if player:
                return 0
            else:
                return 1
        else:
            return 0.5

    def backpropagate(self, result):
        self.wins += result
        self.games += 1
        if self.parent:
            self.parent.backpropagate(result)

    def choose_child(self):
        weights = [c.ucb() for c in self.children]
        child = self.children[np.argmax(weights)]
        return child

    def policy(self):
        current_node = self
        while not current_node.is_terminal():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.choose_child()
        return current_node

    def best_action(self, simulations=50):

        for _ in range(simulations):
            v = self.policy()
            result = 0
            for _ in range(1):
                result += v.rollout(self.game.player)

            v.backpropagate(result)

        if len(self.children) == 0:
            # print("no children")
            return Node()

        best = 0
        best_ch = None
        for c in self.children:
            if c.games > best:
                best = c.games
                best_ch = c
        # print(best)
        return best_ch


starting_point = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
wins = 0
for our_position in tqdm(starting_point):
    r = Reversi()
    # r.draw()
    t = Node(r, None)
    while not r.terminal():
        # print(r.player)
        if r.player == our_position:
            # print("mc:")
            t = Node(r, None)
            a = t.best_action()
            m = a.move
            # t = a
            r.do_move(m)
        else:
            m = r.random_move()
            r.do_move(m)
        # r.draw()
    r.draw()
    if our_position and (r.result() > 0):
        wins += 1
    if (not our_position) and (r.result() < 0):
        wins += 1
    print(wins)
