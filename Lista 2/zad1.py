from itertools import zip_longest
import numpy as np

np.random.seed(42)

def init():
    with open("zad_input.txt", "r") as f_in:
        first_line = f_in.readline()
        first_line = first_line.split()
        rows = int(first_line[0])
        cols = int(first_line[1])
        row_values = []
        col_values = []
        for row in range(rows):
            row_values.append([int(number) for number in f_in.readline().split(' ')])
        for col in range(cols):
            col_values.append([int(number) for number in f_in.readline().split(' ')])
    img = np.zeros((rows, cols), dtype='int64')
    return img, row_values, col_values


def is_block_correct(block, D):
    return opt_dist(block, D) == 0


def is_solved(img, row_vals, col_vals):
    is_solved = True
    for i in range(len(row_vals)):
        if not is_block_correct(img[i, :], row_vals[i]):
            is_solved = False
    for i in range(len(col_vals)):
        if not is_block_correct(img[:, i], col_vals[i]):
            is_solved = False
    return is_solved


def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation

def spaces_to_block(desc, spaces):
    block = []
    for s, d in zip_longest(spaces, desc, fillvalue=0):
        for _ in range(s):
            block.append(0)
        for _ in range(d):
            block.append(1)
        if d:
            block.append(0)
    block.pop(-1)
    return block

def count_diff(block1, block2):
    diffs = 0
    for i in range(len(block1)):
        if block1[i] != block2[i]:
            diffs+=1
    return diffs
#
# def opt_dist(block, desc):
#     places_for_spaces = len(desc) + 1
#     no_of_spaces = len(block) - sum(desc) - len(desc) + 1
#     opt_dist = np.inf
#     for possible_spaces in sums(places_for_spaces, no_of_spaces):
#         dist = count_diff(block, spaces_to_block(desc, list(possible_spaces)))
#         if dist < opt_dist:
#             opt_dist = dist
#     return opt_dist


def opt_dist(seq, blocks):
    max_dist = len(seq)
    dp = np.zeros((len(seq), len(blocks)), dtype='int') + max_dist
    dp[blocks[0]-1][0] = (seq[0:blocks[0]] == 0).sum() + (seq[blocks[0]:] == 1).sum()
    # pierwszy bloczek
    for n in range(blocks[0], len(seq)):
        dp[n][0] = dp[n-1][0]
        if seq[n-blocks[0]] == 1:
            dp[n][0] += 1
        else:
            dp[n][0] -= 1
        if seq[n] == 1:
            dp[n][0] -= 1
        else:
            dp[n][0] += 1
    for n in range(1, len(seq)):
        dp[n][0] = min(dp[n][0], dp[n-1][0])
    for k in range(1, len(blocks)):
        for n in range(blocks[k]+1, len(seq)):
            dp[n][k] = min(dp[n-1][k],
                           dp[n-blocks[k]-1][k-1] + blocks[k] - 2*(seq[n-blocks[k]+1:n+1]==1).sum())

    return dp[len(seq)-1, len(blocks)-1]

def best_px_to_flip(img, idx, rows_or_cols, row_vals, col_vals):
    min, min_idx = np.Inf, np.Inf

    if rows_or_cols:
        for i in range(img.shape[1]):
            temp_img = img.copy()
            temp_img[idx, i] = 1 - temp_img[idx, i]
            v = opt_dist(temp_img[idx, :], row_vals[idx]) + opt_dist(
                temp_img[:, i], col_vals[i]
            )
            if v < min:
                min = v
                min_idx = i
    else:
        for i in range(img.shape[0]):
            temp_img = img.copy()
            temp_img[i, idx] = 1 - temp_img[i, idx]
            v = opt_dist(temp_img[i, :], row_vals[i]) + opt_dist(
                temp_img[:, idx], col_vals[idx]
            )
            if v < min:
                min = v
                min_idx = i
    return min_idx

def preprocess_img(img, row_vals, col_vals):
    for idx in range(len(row_vals)):
        r = row_vals[idx]
        row = np.ones(img.shape[1], dtype='int64')
        places_for_spaces = len(r) + 1
        no_of_spaces = img.shape[1] - sum(r) - len(r) + 1
        for possible_spaces in sums(places_for_spaces, no_of_spaces):
            row = (row & np.array(spaces_to_block(r, list(possible_spaces))))
        img[idx, :] = row

    for idx in range(len(col_vals)):
        c = col_vals[idx]
        col = np.ones(img.shape[0], dtype='int64')
        places_for_spaces = len(c) + 1
        no_of_spaces = img.shape[0] - sum(c) - len(c) + 1
        for possible_spaces in sums(places_for_spaces, no_of_spaces):
            col = (col & np.array(spaces_to_block(c, list(possible_spaces))))
        img[:, idx] = (img[:, idx] | col)

    return img


def random_incorrect_block(img, row_vals, col_vals):

    while True:
        rows_or_cols = np.random.randint(2)
        if rows_or_cols:  # if True -> rows
            idx = np.random.randint(0, img.shape[0])
            if is_block_correct(img[idx, :], row_vals[idx]):
                if np.random.random() < 0.1:
                    return idx, rows_or_cols
                continue
            return idx, rows_or_cols
        else:
            idx = np.random.randint(0, img.shape[1])
            if is_block_correct(img[:, idx], col_vals[idx]):
                if np.random.random() < 0.1:
                    return idx, rows_or_cols
                continue
            return idx, rows_or_cols


def output_img(img):
    with open("zad_output.txt", "w") as f_out:
        proper_img = np.zeros((img.shape[0], img.shape[1]), dtype="<U12")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j]:
                    proper_img[i][j] = "#"
                else:
                    proper_img[i][j] = "."
            s = "".join(proper_img[i, :])
            f_out.write(s + "\n")

def print_img(img):
        proper_img = np.zeros((img.shape[0], img.shape[1]), dtype="<U12")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j]:
                    proper_img[i][j] = "#"
                else:
                    proper_img[i][j] = "."
            s = "".join(proper_img[i, :])
            print(s)


def main_loop():
    img, row_vals, col_vals = init()
    preprocessed_img = preprocess_img(img, row_vals, col_vals)
    img = preprocessed_img.copy()
    iter = 0
    while not is_solved(img, row_vals, col_vals):
        iter += 1
        if not iter % 1000:
            print(iter)
            img = preprocessed_img.copy()
        idx1, rows_or_cols = random_incorrect_block(img, row_vals, col_vals)
        idx2 = best_px_to_flip(img, idx1, rows_or_cols, row_vals, col_vals)
        if rows_or_cols:
            img[idx1, idx2] = 1 - img[idx1, idx2]
        else:
            img[idx2, idx1] = 1 - img[idx2, idx1]
        # img = img | preprocessed_img
    output_img(img)


main_loop()
