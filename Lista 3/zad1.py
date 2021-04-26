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

def update_row_and_masks(idx, possible_row_values,img):
    row = img[idx, :] 
    certain_zeros = np.zeros(len(row), dtype = 'int64')
    certain_ones = np.ones(len(row), dtype = 'int64')
    for possibility in possible_row_values[idx]:
        certain_zeros |= possibility
        certain_ones &= possibility
    for i in range(len(row)):
        if certain_zeros[i] == 0:
            row[i] = 0
        if certain_ones[i] == 1:
            row[i] = 1 
    updated_possibilities = []
    for mask in possible_row_values[idx]:
        if np.all(mask[row == 1] == 1) and np.all(mask[row == 0] == 0):
            updated_possibilities.append(mask)
    possible_row_values[idx] = updated_possibilities
    return

def update_col_and_masks(idx, possible_col_values, img):
    col = img[:, idx]
    certain_zeros = np.zeros(len(col), dtype = 'int64')
    certain_ones = np.ones(len(col), dtype = 'int64')
    
    for possibility in possible_col_values[idx]:
        certain_zeros |= possibility
        certain_ones &= possibility
    for i in range(len(col)):
        if certain_zeros[i] == 0:
            col[i] = 0
        if certain_ones[i] == 1:
            col[i] = 1
    img[:, idx] = col
    updated_possibilities = []
    for mask in possible_col_values[idx]:
        if np.all(mask[col == 1] == 1) and np.all(mask[col == 0] == 0):
            updated_possibilities.append(mask)
    possible_col_values[idx] = updated_possibilities
    return

def print_img(img):
    proper_img = np.zeros((img.shape[0], img.shape[1]), dtype="<U12")
    with open("zad_output.txt", "w") as f_out:
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j] == 1:
                    proper_img[i][j] = "#"
                else:
                    proper_img[i][j] = "."
            s = "".join(proper_img[i, :])
            f_out.write(s + "\n")

def main_loop():
    img, row_vals, col_vals = init()
    possible_row_values, possible_col_values = prepare_possibilities(img, row_vals, col_vals)
    while np.any(img == -1):
        for i in range(img.shape[0]):
            update_row_and_masks(i, possible_row_values, img)
        for i in range(img.shape[1]):
            update_col_and_masks(i, possible_col_values, img)
    print_img(img)

    
main_loop()
