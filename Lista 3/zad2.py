from itertools import zip_longest
import numpy as np

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
    img = np.zeros((rows, cols), dtype='int64') - 1
    return img, row_values, col_values

def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation

def spaces_to_block(desc, spaces):
    block = []
    for s, d in zip_longest(spaces, desc, fillvalue = 0):
        for _ in range(s):
            block.append(0)
        for _ in range(d):
            block.append(1)
        if d:
            block.append(0)
    block.pop(-1)
    return block

def prepare_possibilities(img, row_vals, col_vals):
    possible_row_values = [[] for _ in range(len(row_vals))]
    for idx in range(len(row_vals)):
        r = row_vals[idx]
        places_for_spaces = len(r) + 1
        no_of_spaces = img.shape[1] - sum(r) - len(r) + 1
        for possible_spaces in sums(places_for_spaces, no_of_spaces):
            possible_row_values[idx].append(np.array(spaces_to_block(r, list(possible_spaces))))
    possible_col_values = [[] for _ in range(len(col_vals))]
    for idx in range(len(col_vals)):
        c = col_vals[idx]
        places_for_spaces = len(c) + 1
        no_spaces = img.shape[0] - sum(c) - len(c) + 1
        for possible_spaces in sums(places_for_spaces, no_spaces):
            possible_col_values[idx].append(np.array(spaces_to_block(c, list(possible_spaces))))
    return possible_row_values, possible_col_values

def update_row_and_masks(idx, possible_row_values, img):
    row = img[idx, :]
    certain_zeros = np.zeros(len(row), dtype = 'int64')
    certain_ones = np.ones(len(row), dtype = 'int64')
    changed = False
    possible_to_solve = True
    for possibility in possible_row_values[idx]:
        certain_zeros |= possibility
        certain_ones &= possibility
    for i in range(len(row)):
        if certain_zeros[i] == 0 and row[i] == -1:
            changed = True
            row[i] = 0
        if certain_ones[i] == 1 and row[i] == -1:
            changed = True
            row[i] = 1
    updated_possibilities = []
    for mask in possible_row_values[idx]:
        if np.all(mask[row == 1] == 1) and np.all(mask[row == 0] == 0):
            updated_possibilities.append(mask)
    if len(updated_possibilities) == 0:
        possible_to_solve = False
    possible_row_values[idx] = updated_possibilities.copy()
    return changed, possible_to_solve

def update_col_and_masks(idx, possible_col_values, img):
    col = img[:, idx]
    certain_zeros = np.zeros(len(col), dtype = 'int64')
    certain_ones = np.ones(len(col), dtype = 'int64')
    changed = False
    possible_to_solve = True
    for possibility in possible_col_values[idx]:
        certain_zeros |= possibility
        certain_ones &= possibility
    for i in range(len(col)):
        if certain_zeros[i] == 0 and col[i] == -1:
            changed = True
            col[i] = 0
        if certain_ones[i] == 1 and col[i] == -1:
            changed = True
            col[i] = 1
    img[:, idx] = col
    updated_possibilities = []
    for mask in possible_col_values[idx]:
        if np.all(mask[col == 1] == 1) and np.all(mask[col == 0] == 0):
            updated_possibilities.append(mask)
    if len(updated_possibilities) == 0:
        possible_to_solve = False
    possible_col_values[idx] = updated_possibilities.copy()
    return changed, possible_to_solve

def print_img(img):
        proper_img = np.zeros((img.shape[0], img.shape[1]), dtype="<U12")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j] == 1:
                    proper_img[i][j] = "#"
                elif img[i][j] == 0:
                    proper_img[i][j] = "."
                else:
                    proper_img[i][j] = "?"
            s = "".join(proper_img[i, :])
            print(s)

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


def update_masks_for_val(idx, block, masks):
    updated_possibilities = []
    for mask in masks[idx]:
        if np.all(mask[block == 1] == 1) and np.all(mask[block == 0] == 0):
            updated_possibilities.append(mask)
    return updated_possibilities

def infer(img, possible_row_values, possible_col_values):
    while True:
        changed = False
        possible_to_solve = True
        for i in range(img.shape[0]):
            c, p = update_row_and_masks(i, possible_row_values, img)
            changed |= c
            possible_to_solve &= p
        for i in range(img.shape[1]):
            c, p = update_col_and_masks(i, possible_col_values, img)
            changed |= c
            possible_to_solve &= p
        if not changed:
            break
    return possible_to_solve

def is_unfinished(img):
    return np.any(img == -1)

def solve(img, possible_row_values, possible_col_values, tested):
    while is_unfinished(img):
        possible_to_solve = infer(img, possible_row_values, possible_col_values)
        # if(len(np.dstack(np.where(img == -1))[0]) == 0):
        #     print_img(img)
        if not possible_to_solve:
            return False
        unknown = np.dstack(np.where(img == -1))[0]
        # np.random.shuffle(unknown)
        # print(unknown.shape[0])
        for px in unknown:
            if (px[0] + px[1] * 300) in tested:
                continue
            tested.add(px[0] + px[1] * 300)
            copied_img = img.copy()
            copied_col = possible_col_values.copy()
            copied_row = possible_row_values.copy()
            copied_img[tuple(px)] = 1
            row = copied_img[px[0], :]
            copied_row[px[0]] = update_masks_for_val(px[0], row, copied_row)
            col = copied_img[:, px[1]]
            copied_col[px[1]] = update_masks_for_val(px[1], col, copied_col)
            if (solve(copied_img, copied_row, copied_col, tested.copy())):
                return True
            copied_img = img.copy()
            copied_col = possible_col_values.copy()
            copied_row = possible_row_values.copy()
            copied_img[tuple(px)] = 0
            row = copied_img[px[0], :]
            copied_row[px[0]] = update_masks_for_val(px[0], row, copied_row)
            col = copied_img[:, px[1]]
            copied_col[px[1]] = update_masks_for_val(px[1], col, copied_col)
            if(solve(copied_img, copied_row, copied_col, tested.copy())):
                return True
            return False
    output_img(img)
    return True


def main_loop():
    img, row_vals, col_vals = init()
    possible_row_values, possible_col_values = prepare_possibilities(img, row_vals,col_vals)
    solve(img, possible_row_values, possible_col_values, set())

main_loop()
