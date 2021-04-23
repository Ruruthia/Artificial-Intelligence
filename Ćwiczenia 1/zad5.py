import numpy as np
from itertools import combinations


blots = np.array([i for i in range(2, 11) for _ in range(4)])
figs = np.array([i for i in range(11, 15) for _ in range(4)])


def classify_hand(hand, color):

    pairs = 0
    thirds = 0
    hand.sort()
    hand = list(hand)
    straight = False
    eval = 1
    for card in set(hand):
        if hand.count(card) == 2:
            eval = max(eval, 2)
            pairs += 1
        if hand.count(card) == 3:
            eval = max(eval, 4)
            thirds += 1
        if hand.count(card) == 4:
            eval = max(eval, 8)
    if hand[4] - hand[0] == 4 and len(set(hand)) == 5:
        straight = True
        eval = max(eval, 5)
    if color:
        eval = max(eval, 6)
    if pairs == 2:
        eval = max(eval, 3)
    if pairs == 1 and thirds == 1:
        eval = max(eval, 7)
    if color and straight:
        eval = max(eval, 9)
    return eval


def count_combinations(size, type):
    counts = np.zeros(9)
    comb = combinations(range(size), 5)
    for cards in list(comb):
        color = False
        colors = [0] * 4
        for card in cards:
            colors[card % 4] += 1
        if colors[card % 4] == 5:
            color = True
        cards = np.array(cards)
        if type == "blots":
            cards = blots[cards]
        if type == "figs":
            cards = figs[cards]
        counts[classify_hand(cards, color) - 1] += 1
    return counts


def main():
    blots_count = count_combinations(36, "blots")
    figs_count = count_combinations(16, "figs")
    blots_count = blots_count / blots_count.sum()
    figs_count = figs_count / figs_count.sum()
    p = 0
    for i in range(1, 9):
        for j in range(i):
            p += blots_count[i] * figs_count[j]
    print(f"Prawdopodobieństwo wygranej blotkarza: {p * 100:.4f} %")


main()


# def random_figure_hand(figs):
#     cards = np.random.choice(len(figs) - 1, 5, replace=False)
#     color = False
#     colors = [0] * 4
#     for card in cards:
#         colors[card % 4] += 1
#         if colors[card % 4] == 5:
#             color = True
#     return figs[cards], color
#

#
