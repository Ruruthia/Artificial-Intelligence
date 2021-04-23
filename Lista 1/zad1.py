def print_board(board):
    for i in range(8):
        print(board[i])
    print("")


def make_board(position):
    board = [[".." for _ in range(8)] for _ in range(8)]
    wk = position[6:8]
    wr = position[9:11]
    bk = position[12:14]
    board[int(bk[1]) - 1][ord(bk[0]) - 97] = "BK"
    board[int(wk[1]) - 1][ord(wk[0]) - 97] = "WK"
    board[int(wr[1]) - 1][ord(wr[0]) - 97] = "WR"
    return board


def checked_by_black(position):
    board = [[0 for _ in range(8)] for _ in range(8)]
    bk = position[12:14]
    for i in [ord(bk[0]) - 98, ord(bk[0]) - 97, ord(bk[0]) - 96]:
        if i < 0 or i >= 8:
            continue
        for j in [int(bk[1]) - 2, int(bk[1]) - 1, int(bk[1])]:
            if j < 0 or j >= 8:
                continue
            board[j][i] = 1
    return board


def checked_by_white(position):
    board = [[0 for _ in range(8)] for _ in range(8)]
    wk = position[6:8]
    wr = position[9:11]
    for i in [ord(wk[0]) - 98, ord(wk[0]) - 97, ord(wk[0]) - 96]:
        if i < 0 or i >= 8:
            continue
        for j in [int(wk[1]) - 2, int(wk[1]) - 1, int(wk[1])]:
            if j < 0 or j >= 8:
                continue
            board[j][i] = 1
    board[int(wk[1]) - 1][ord(wk[0]) - 97] = 3
    r_row = int(wr[1]) - 1
    r_col = ord(wr[0]) - 97
    for i in range(8):
        board[r_row][i] = 1
        board[i][r_col] = 1
    board[r_row][r_col] = 2
    return board


def checked_by_white_king(position):
    board = [[0 for _ in range(8)] for _ in range(8)]
    wk = position[6:8]
    wr = position[9:11]
    for i in [ord(wk[0]) - 98, ord(wk[0]) - 97, ord(wk[0]) - 96]:
        if i < 0 or i >= 8:
            continue
        for j in [int(wk[1]) - 2, int(wk[1]) - 1, int(wk[1])]:
            if j < 0 or j >= 8:
                continue
            board[j][i] = 1
    return board


def checked_by_white_rook(position):
    board = [[0 for _ in range(8)] for _ in range(8)]
    wr = position[9:11]
    r_row = int(wr[1]) - 1
    r_col = ord(wr[0]) - 97
    for i in range(8):
        board[r_row][i] = 1
        board[i][r_col] = 1
    board[r_row][r_col] = 2
    return board


def is_king_checked(position):
    if position[:5] == "white":
        return False
    checked = True
    bk = position[12:14]
    blocked_by_white = checked_by_white(position)
    for i in [ord(bk[0]) - 98, ord(bk[0]) - 97, ord(bk[0]) - 96]:
        if i < 0 or i >= 8:
            continue
        for j in [int(bk[1]) - 2, int(bk[1]) - 1, int(bk[1])]:
            if j < 0 or j >= 8:
                continue
            if (i == ord(bk[0]) - 97) and (j == int(bk[1]) - 1):
                continue
            if (
                blocked_by_white[j][i] == 2
                and not checked_by_white_king(position)[j][i]
            ):
                checked = False
            if not blocked_by_white[j][i]:
                checked = False
    return checked


def generate_possible_moves(position):
    possible_moves = []
    if position[:5] == "black":
        blocked_by_white = checked_by_white(position)
        bk_col = position[12]
        bk_row = position[13]
        pos_cols = [chr(ord(bk_col) + 1), bk_col, chr(ord(bk_col) - 1)]
        pos_rows = [int(bk_row) + 1, int(bk_row), int(bk_row) - 1]
        for col in pos_cols:
            if col == "`" or col == "i":
                continue
            for row in pos_rows:
                if (
                    ((col == bk_col) and (str(row) == bk_row))
                    or (row == 0)
                    or (row == 9)
                ):
                    continue

                new_position = "white " + position[6:12] + str(col) + str(row)
                if not blocked_by_white[row - 1][ord(col) - 97]:
                    possible_moves.append(new_position)

    if position[:5] == "white":

        blocked_by_black = checked_by_black(position)
        wk_col = position[6]
        wk_row = position[7]
        pos_cols = [chr(ord(wk_col) + 1), wk_col, chr(ord(wk_col) - 1)]
        pos_rows = [int(wk_row) + 1, int(wk_row), int(wk_row) - 1]
        for col in pos_cols:
            if col == "`" or col == "i":
                continue
            for row in pos_rows:
                if (
                    ((col == wk_col) and (str(row) == wk_row))
                    or (row == 0)
                    or (row == 9)
                ):
                    continue
                new_position = "black " + str(col) + str(row) + position[8:]
                if not blocked_by_black[row - 1][ord(col) - 97]:
                    possible_moves.append(new_position)
        wr_col = position[9]
        wr_row = position[10]
        for i in range(1, 9):
            if str(i) == wr_row:
                continue
            new_position = "black " + position[6:9] + wr_col + str(i) + position[11:]
            possible_moves.append(new_position)
        for i in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            if i == wr_col:
                continue
            new_position = "black " + position[6:9] + i + wr_row + position[11:]
            possible_moves.append(new_position)
    return possible_moves


def bfs(position):
    set_of_states = set()
    set_of_states.add(position)
    queue = [position]
    depth = 0
    play = {position: ""}
    while queue:
        depth += 1
        queue_len = len(queue)
        while queue_len > 0:
            s = queue.pop(0)
            for move in generate_possible_moves(s):
                if move not in set_of_states:
                    play[move] = str(play[s]) + move + "\n"
                    if is_king_checked(move):
                        # return depth
                        return depth, play[move]
                    set_of_states.add(move)
                    queue.append(move)
            queue_len -= 1


d, m = bfs("black g8 h1 c4")
print(d)  # 9
for line in m.splitlines():
    print(line)
    print_board(make_board(line))
# 6
# print(bfs("black b4 f3 e8"))
# # print(d)  # 9
# # for line in m.splitlines():
# #     print(line)
# #     print_board(make_board(line))
# print(bfs("white h6 a4 d4"))
# print(bfs("black b4 f3 e8"))
# print(bfs("white a1 e3 b7"))  # 9
# print(bfs("black h7 a2 f2"))  # 6
# print(bfs("black a2 e4 a4"))  # 8
# print(bfs("black g8 h1 c4"))  # 10

# with open("zad1_input.txt", "r") as f_in:
#     with open("zad1_output.txt", "w") as f_out:
#         for line in f_in:
#             f_out.write(str(bfs(line)) + "\n")
