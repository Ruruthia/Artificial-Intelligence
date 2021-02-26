import numpy as np


def read_dict(file):
    my_set = set()
    max_len = 0
    with open(file, "r") as f:
        for word in f:
            word = word.strip()
            my_set.add(word)
            if len(word) > max_len:
                max_len = len(word)
    return my_set, max_len


def split_text(text, set, max_len):
    cost = [0] * (len(text) + 1)
    words = [0] * (len(text) + 1)
    for start in range(len(text) - 1):
        for stop in range(start + 1, min(start + max_len - 1, len(text) + 1)):
            if text[start:stop] in set:
                if (cost[start] + (stop - start) ** 2) > cost[stop]:
                    cost[stop] = cost[start] + (stop - start) ** 2
                    words[stop] = start
    return words


def insert_spaces(text, words):
    line = []
    i = len(text)
    while i > 0:
        line.append(text[words[i] : i])
        i = words[i]
    return " ".join(line[::-1])


def process_text(file, dict):
    set, max_len = read_dict(dict)

    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            spaces = split_text(line, set, max_len)
            line = insert_spaces(line, spaces)
            print(line)


process_text("pan_tadeusz_bez_spacji.txt", "polish_words.txt")
