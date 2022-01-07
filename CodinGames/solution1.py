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
            return "WAIT"
        elif self.type == ActionType.SEED:
            return f"SEED {self.origin_cell_id} {self.target_cell_id}"
        else:
            return f"{self.type.name} {self.target_cell_id}"

    @staticmethod
    def parse(action_string):
        split = action_string.split(" ")
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
        self.max_seeds = 2
        self.max_1 = 3
        self.max_2 = 3
        self.max_3 = 4
        self.day = 0
        self.nutrients = 0
        self.board = {}
        self.cell_richness = {}
        self.my_trees = []
        self.my_trees0 = []
        self.my_trees0_active = []
        self.my_trees1 = []
        self.my_trees1_active = []
        self.my_trees2 = []
        self.my_trees2_active = []
        self.my_trees3 = []
        self.my_trees3_active = []
        self.my_trees_dict = {}
        self.opp_trees = []
        self.opp_trees_dict = {}
        self.possible_actions = []
        self.my_sun = 0
        self.my_score = 0
        self.opponents_sun = 0
        self.opponent_score = 0
        self.opponent_is_waiting = 0

    def sort_trees_by_richness(self, trees):
        tree_indices = []
        indices_richness = []
        for tree in trees:
            tree_indices.append(tree.cell_index)
            indices_richness.append(self.cell_richness[tree.cell_index])
        tree_indices = np.array(tree_indices)
        tree_indices = tree_indices[np.argsort(indices_richness)[::-1]]
        tree_indices = list(tree_indices)
        return tree_indices

    def compute_possible_seeds(self):
        self.possible_seeds = {}
        for tree in self.my_trees:
            if not tree.is_dormant:
                size = tree.size
                if size > 0:
                    cells = [self.board[tree.cell_index]]
                    while size > 0:
                        depth = len(cells)
                        for _ in range(depth):
                            cell = cells.pop(0)
                            for neighbour in cell.neighbors:
                                if neighbour != -1:
                                    neighbour = self.board[neighbour]
                                    if neighbour.richness != 0 and neighbour.cell_index not in self.opp_trees_dict and neighbour.cell_index not in self.my_trees_dict:
                                        if neighbour.cell_index not in self.possible_seeds:
                                            self.possible_seeds[neighbour.cell_index] = set()
                                        self.possible_seeds[neighbour.cell_index].add(tree.cell_index)
                                    cells.append(neighbour)
                        size -= 1

    def compute_costs(self):
        cost0 = len(self.my_trees0)
        cost1 = len(self.my_trees1) + 1
        cost2 = len(self.my_trees2) + 3
        cost3 = len(self.my_trees3) + 7
        return [cost0, cost1, cost2, cost3]


number_of_cells = int(input())
game = Game()
for i in range(number_of_cells):
    cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [
        int(j) for j in input().split()
    ]
    game.board[cell_index] = Cell(cell_index, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5])

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
    game.my_trees.clear()
    game.my_trees0.clear()
    game.my_trees0_active.clear()
    game.my_trees1.clear()
    game.my_trees1_active.clear()
    game.my_trees2.clear()
    game.my_trees2_active.clear()
    game.my_trees3.clear()
    game.my_trees3_active.clear()
    game.opp_trees.clear()
    for i in range(number_of_trees):
        inputs = input().split()
        cell_index = int(inputs[0])
        size = int(inputs[1])
        is_mine = inputs[2] != "0"
        is_dormant = inputs[3] != "0"
        if is_mine:
            game.my_trees.append(Tree(cell_index, size, True, is_dormant))
            game.my_trees_dict[cell_index] = size
            if size == 0:
                game.my_trees0.append(Tree(cell_index, size, True, is_dormant))
                if not is_dormant:
                    game.my_trees0_active.append(Tree(cell_index, size, True, is_dormant))
            if size == 1:
                game.my_trees1.append(Tree(cell_index, size, True, is_dormant))
                if not is_dormant:
                    game.my_trees1_active.append(Tree(cell_index, size, True, is_dormant))
            if size == 2:
                game.my_trees2.append(Tree(cell_index, size, True, is_dormant))
                if not is_dormant:
                    game.my_trees2_active.append(Tree(cell_index, size, True, is_dormant))
            if size == 3:
                game.my_trees3.append(Tree(cell_index, size, True, is_dormant))
                if not is_dormant:
                    game.my_trees3_active.append(Tree(cell_index, size, True, is_dormant))
        else:
            game.opp_trees.append(Tree(cell_index, size, False, is_dormant))
            game.opp_trees_dict[cell_index] = size

    number_of_possible_actions = int(input())
    game.possible_actions.clear()

    for i in range(number_of_possible_actions):
        possible_action = input()
        game.possible_actions.append(Action.parse(possible_action))
    game.compute_possible_seeds()
    if game.day == 0:
        print("WAIT")
    elif game.day == 1:
        if game.my_sun > 2:
            print("GROW " + str(game.my_trees[0].cell_index))
        else:
            print("WAIT")
    elif game.day == 2:
        if game.my_sun > 1:
            print("GROW " + str(game.my_trees[1].cell_index))
        elif len(game.my_trees) == 2:
            first_tree = game.my_trees[0].cell_index
            second_tree = game.my_trees[1].cell_index
            places_to_seed = [x for x in game.possible_seeds if first_tree in game.possible_seeds[x]]
            print("SEED " + str(first_tree) + " " + str(random.choice(places_to_seed)))
        else:
            print("WAIT")
    elif game.day == 3:
        if game.my_sun > 3:
            print("GROW " + str(game.my_trees0[0].cell_index))
        elif len(game.my_trees1) == 1 and len(game.my_trees0) == 0:
            places_to_seed = [x for x in game.possible_seeds if second_tree in game.possible_seeds[x]]
            print("SEED " + str(second_tree) + " " + str(random.choice(places_to_seed)))
        else:
            print("WAIT")

    ##### co w międzyczasie?
    ##### stosunek liczby drzew różnego rozmiaru zależny od czasu - im później tym więcej 3? potrzebuję więcej kasy

    elif game.day == 21:
        if len(game.my_trees3_active) > 0 and game.my_sun >=4:
            print("COMPLETE " + str(game.my_trees3_active.pop(0).cell_index))
        elif len(game.my_trees2_active) > 0 and game.my_sun >= game.compute_costs()[3]:
            print("GROW " + str(game.my_trees2_active.pop(0).cell_index))
        elif len(game.my_trees1_active) > 0 and game.my_sun >= game.compute_costs()[2]:
            print("GROW " + str(game.my_trees1_active.pop(0).cell_index))
        else:
            print("WAIT")

    elif game.day == 22:
        if len(game.my_trees3_active) > 0 and game.my_sun >=4:
            print("COMPLETE " + str(game.my_trees3_active.pop(0).cell_index))
        elif len(game.my_trees2_active) > 0 and game.my_sun >= game.compute_costs()[3]:
            print("GROW " + str(game.my_trees2_active.pop(0).cell_index))
        else:
            print("WAIT")

    elif game.day == 23:
        print("OSTATNI", flush = True, file = sys.stderr)
        if len(game.my_trees3) > 0 and game.my_sun >=4:
            print("COMPLETE " + str(game.my_trees3.pop(0).cell_index))
        else:
            print("WAIT")
    else:
        print("normal day", flush = True, file = sys.stderr)
        if len(game.my_trees0) < game.max_seeds and len(game.my_trees0) <= len(game.my_trees1) and game.compute_costs()[0] < game.my_sun and len(list(game.possible_seeds.keys())) > 0 and game.day < 18:
            cell_to_seed = random.choice(list(game.possible_seeds.keys()))
            tree_to_seed = random.choice(list(game.possible_seeds[cell_to_seed]))
            print("SEED " + str(tree_to_seed) + " " + str(cell_to_seed))
        elif len(game.my_trees1) < game.max_1 and len(game.my_trees1) <= len(game.my_trees0) and len(game.my_trees0_active) > 0 and game.compute_costs()[1] < game.my_sun:
            sorted_trees = game.sort_trees_by_richness(game.my_trees0_active)
            print("GROW " + str(sorted_trees[0]))
        elif len(game.my_trees2) < game.max_2 and len(game.my_trees2) <= len(game.my_trees1) and len(game.my_trees1_active) > 0 and game.compute_costs()[2] < game.my_sun:
            sorted_trees = game.sort_trees_by_richness(game.my_trees1_active)
            print("GROW " + str(sorted_trees[0]))
        elif len(game.my_trees3) < game.max_3 and len(game.my_trees3) <= len(game.my_trees2) and len(game.my_trees2_active) > 0 and game.compute_costs()[3] < game.my_sun:
            sorted_trees = game.sort_trees_by_richness(game.my_trees2_active)
            print("GROW " + str(sorted_trees[0]))
        elif len(game.my_trees3_active) > 2 and 4 <= game.my_sun:
            sorted_trees = game.sort_trees_by_richness(game.my_trees3_active)
            print("COMPLETE " + str(sorted_trees[0]))
        else:
            print("WAIT")
