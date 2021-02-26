import numpy as np

blots = np.array([i for i in range(2, 11) for _ in range(4)])
figs = np.array([i for i in range(11, 15) for _ in range(4)])


def random_blots_hand(blots):
    cards = np.random.choice(len(blots) - 1, 5, replace=False)
    color = False
    colors = [0] * 4
    for card in cards:
        colors[card % 4] += 1
        if colors[card % 4] == 5:
            color = True
    return blots[cards], color


def random_figure_hand(figs):
    cards = np.random.choice(len(figs) - 1, 5, replace=False)
    color = False
    colors = [0] * 4
    for card in cards:
        colors[card % 4] += 1
        if colors[card % 4] == 5:
            color = True
    return figs[cards], color


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


def did_blotter_win(blots_hand, blots_color, figure_hand, figure_color):
    return classify_hand(blots_hand, blots_color) > classify_hand(
        figure_hand, figure_color
    )


def simulation(iters):
    wins = 0
    for i in range(iters):
        hb, cb = random_blots_hand(blots)
        hf, cf = random_figure_hand(figs)
        if did_blotter_win(hb, cb, hf, cf):
            wins += 1
    print(100 - 100 * wins / iters)


simulation(10000000)
