import sys
import math
from enum import Enum
import random
import numpy as np

class Cell:
    def __init__(self, cell_index, richness, neighbors):
        self.cell_index = cell_index
        self.richness = richness
        self.neighbors = neighbors

class Tree:
    def __init__(self, cell_index, size, is_mine, is_dormant):
        self.cell_index = cell_index
        self.size = size
        self.is_mine = is_mine
        self.is_dormant = is_dormant

class ActionType(Enum):
    WAIT = "WAIT"
    SEED = "SEED"
    GROW = "GROW"
    COMPLETE = "COMPLETE"

class Action:
    def __init__(self, type, target_cell_id=None, origin_cell_id=None):
        self.type = type
        self.target_cell_id = target_cell_id
        self.origin_cell_id = origin_cell_id

    def __str__(self):
        if self.type == ActionType.WAIT:
            return 'WAIT'
        elif self.type == ActionType.SEED:
            return f'SEED {self.origin_cell_id} {self.target_cell_id}'
        else:
            return f'{self.type.name} {self.target_cell_id}'

    @staticmethod
    def parse(action_string):
        split = action_string.split(' ')
        if split[0] == ActionType.WAIT.name:
            return Action(ActionType.WAIT)
        if split[0] == ActionType.SEED.name:
            return Action(ActionType.SEED, int(split[2]), int(split[1]))
        if split[0] == ActionType.GROW.name:
            return Action(ActionType.GROW, int(split[1]))
        if split[0] == ActionType.COMPLETE.name:
            return Action(ActionType.COMPLETE, int(split[1]))

class Game:
    def __init__(self):
        self.day = 0
        self.nutrients = 0
        self.board = []
        self.cell_richness = {}
        self.trees = []
        self.possible_actions = []
        self.my_sun = 0
        self.my_score = 0
        self.opponents_sun = 0
        self.opponent_score = 0
        self.opponent_is_waiting = 0
        self.tree_indices2 = []
        self.tree_indices = []

    def sort_grown_trees_by_richness(self):
        self.tree_indices = []
        indices_richness = []
        for tree in self.trees:
            if tree.is_mine and tree.size == 3:
                self.tree_indices.append(tree.cell_index)
                indices_richness.append(self.cell_richness[tree.cell_index])
        self.tree_indices = np.array(self.tree_indices)
        self.tree_indices = self.tree_indices[np.argsort(indices_richness)[::-1]]
        self.tree_indices = list(self.tree_indices)

    def sort_ungrown_trees_by_richness(self):
        self.tree_indices2 = []
        indices_richness = []
        for tree in self.trees:
            if tree.is_mine and tree.size < 3:
                self.tree_indices2.append(tree.cell_index)
                indices_richness.append(self.cell_richness[tree.cell_index])
        self.tree_indices2 = np.array(self.tree_indices2)
        self.tree_indices2 = self.tree_indices2[np.argsort(indices_richness)[::-1]]
        self.tree_indices2 = list(self.tree_indices2)

    def compute_next_action(self, sun):
        if sun > 3 and len(self.tree_indices) > 0:
            print("before!", file=sys.stderr)
            print("COMPLETE " + str(self.tree_indices.pop(0)))
            print("after!", file=sys.stderr)
            sun-= 4
        elif sun > 3 and len(self.tree_indices2) > 0:
            print("GROW " + str(self.tree_indices2.pop(0)))
            sun -= 4
        else:
            print("WAIT")


number_of_cells = int(input())
game = Game()
for i in range(number_of_cells):
    cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]
    game.board.append(Cell(cell_index, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]))
    game.cell_richness[cell_index] = richness

while True:
    _day = int(input())
    game.day = _day
    nutrients = int(input())
    game.nutrients = nutrients
    sun, score = [int(i) for i in input().split()]
    game.my_sun = sun
    game.my_score = score
    opp_sun, opp_score, opp_is_waiting = [int(i) for i in input().split()]
    game.opponent_sun = opp_sun
    game.opponent_score = opp_score
    game.opponent_is_waiting = opp_is_waiting
    number_of_trees = int(input())
    game.trees.clear()
    for i in range(number_of_trees):
        inputs = input().split()
        cell_index = int(inputs[0])
        size = int(inputs[1])
        is_mine = inputs[2] != "0"
        is_dormant = inputs[3] != "0"
        game.trees.append(Tree(cell_index, size, is_mine == 1, is_dormant))

    number_of_possible_actions = int(input())
    game.possible_actions.clear()
    for i in range(number_of_possible_actions):
        possible_action = input()
        game.possible_actions.append(Action.parse(possible_action))

    game.sort_grown_trees_by_richness()
    game.sort_ungrown_trees_by_richness()
    game.compute_next_action(sun)
