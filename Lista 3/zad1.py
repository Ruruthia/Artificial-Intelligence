

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

def opt_dist(block, desc):
    places_for_spaces = len(desc) + 1
    no_of_spaces = len(block) - sum(desc) - len(desc) + 1
    opt_dist = np.inf
    for possible_spaces in sums(places_for_spaces, no_of_spaces):
        dist = count_diff(block, spaces_to_block(desc, list(possible_spaces)))
        if dist < opt_dist:
            opt_dist = dist
    return opt_dist

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
