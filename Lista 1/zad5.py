import numpy as np


def init():
    with open("zad5_input.txt", "r") as f_in:
        first_line = f_in.readline()
        first_line = first_line.split()
        rows = int(first_line[0])
        cols = int(first_line[1])
        row_values = np.zeros(rows)
        col_values = np.zeros(cols)
        for row in range(rows):
            row_values[row] = int(f_in.readline().strip())
        for col in range(cols):
            col_values[col] = int(f_in.readline().strip())
    img = np.zeros((rows, cols))
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


def opt_dist(block, D):
    switch = 0
    start = 0
    D = int(D)
    for i in range(D):
        if not block[i]:
            switch += 1
    for i in range(D, len(block)):
        if block[i]:
            switch += 1
    min = switch
    while start + D < len(block):
        start += 1
        if block[start - 1]:
            switch += 2
        if block[start + D - 1]:
            switch -= 2
        if switch < min:
            min = switch
    return min


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


def random_incorrect_block(img, row_vals, col_vals):

    while True:
        rows_or_cols = np.random.randint(2)
        if rows_or_cols:  # if True -> rows
            idx = np.random.randint(0, img.shape[0])
            if is_block_correct(img[idx, :], row_vals[idx]):
                if np.random.random() < 0.05:
                    return idx, rows_or_cols
                continue
            return idx, rows_or_cols
        else:
            idx = np.random.randint(0, img.shape[1])
            if is_block_correct(img[:, idx], col_vals[idx]):
                if np.random.random() < 0.05:
                    return idx, rows_or_cols
                continue
            return idx, rows_or_cols


def output_img(img):
    with open("zad5_output.txt", "w") as f_out:
        proper_img = np.zeros((img.shape[0], img.shape[1]), dtype="<U12")
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j]:
                    proper_img[i][j] = "#"
                else:
                    proper_img[i][j] = "."
            s = "".join(proper_img[i, :])
            f_out.write(s + "\n")


def main_loop():
    img, row_vals, col_vals = init()
    iter = 0
    while not is_solved(img, row_vals, col_vals):
        iter += 1
        if not iter % 100:
            img = np.zeros((len(row_vals), len(col_vals)))
        idx1, rows_or_cols = random_incorrect_block(img, row_vals, col_vals)
        idx2 = best_px_to_flip(img, idx1, rows_or_cols, row_vals, col_vals)
        if rows_or_cols:
            img[idx1, idx2] = 1 - img[idx1, idx2]
        else:
            img[idx2, idx1] = 1 - img[idx2, idx1]
    output_img(img)


main_loop()
