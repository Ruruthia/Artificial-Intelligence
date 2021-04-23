# ------------------------------------
def is_checked(position):
    wk = position[6:8]
    wr = position[9:11]
    bk = position[12:14]
    checked_on_wall = (
        ((bk[0] == "a") and (wr[0] == "a") and (bk[1] == wk[1]) and (wk[0] == "c"))
        or ((bk[0] == "h") and (wr[0] == "h") and (bk[1] == wk[1]) and (wk[0] == "f"))
        or ((bk[1] == "1") and (wr[1] == "1") and (bk[0] == wk[0]) and (wk[1] == "3"))
        or ((bk[1] == "8") and (wr[1] == "8") and (bk[0] == wk[0]) and (wk[1] == "6"))
    )
    checked_on_corner = (
        ((bk == "a8") and (wr[0] == "a" and ((wk == "c7") or (wk == "c8"))))
        or ((bk == "a8") and (wr[1] == "8" and ((wk == "a6") or (wk == "b6"))))
        or ((bk == "a8") and (wr == "b7"))
        or ((bk == "a1") and (wr[0] == "a" and ((wk == "c1") or (wk == "c2"))))
        or ((bk == "a1") and (wr[1] == "1" and ((wk == "a3") or (wk == "b3"))))
        or ((bk == "a1") and (wr == "b2"))
        or ((bk == "h8") and (wr[0] == "h" and ((wk == "f7") or (wk == "f8"))))
        or ((bk == "h8") and (wr[1] == "8" and ((wk == "h6") or (wk == "g6"))))
        or ((bk == "h8") and (wr == "g7"))
        or ((bk == "h1") and (wr[0] == "h" and ((wk == "f1") or (wk == "f2"))))
        or ((bk == "h1") and (wr[1] == "1" and ((wk == "h3") or (wk == "g3"))))
        or ((bk == "h1") and (wr == "g2"))
    )
    return checked_on_wall or checked_on_corner


def generate_possible_moves(position):
    possible_moves = []
    if position[:5] == "black":
        bk_col = position[12]
        bk_row = position[13]
        pos_cols = [chr(ord(bk_col) + 1), bk_col, chr(ord(bk_col) - 1)]
        pos_rows = [int(bk_row) + 1, int(bk_row), int(bk_row) - 1]
        for col in pos_cols:
            if col == "`" or col == "i":
                continue
            for row in pos_rows:
                if (col == bk_col) and (str(row) == bk_row) or row == 0 or row == 9:
                    continue
                new_position = "white " + position[6:12] + str(col) + str(row)
                if not is_checked(new_position):
                    possible_moves.append(new_position)

    if position[:5] == "white":
        wk_col = position[6]
        wk_row = position[7]
        pos_cols = [chr(ord(wk_col) + 1), wk_col, chr(ord(wk_col) - 1)]
        pos_rows = [int(wk_row) + 1, int(wk_row), int(wk_row) - 1]
        for col in pos_cols:
            if col == "`" or col == "i":
                continue
            for row in pos_rows:
                if (col == wk_col) and (str(row) == wk_row) or row == 0 or row == 9:
                    continue
                # new_position = " " + position[6:12] + str(col) + str(row)
                # if not is_checked(new_position):
                #     possible_moves.append(new_position)
        return possible_moves


# print(generate_possible_moves("black b1 e3 a5"))
#
# # Na środku planszy
# checked = (
#     (
#         (wr[0] == chr(ord(bk[0]) + 1))
#         and (wk[0] == chr(ord(bk[0]) - 1))
#         and (wk[1] == bk[1])
#     )
#     or (
#         (wr[0] == chr(ord(bk[0]) - 1))
#         and (wk[0] == chr(ord(bk[0]) + 1))
#         and (wk[1] == bk[1])
#     )
#     or (
#         (wr[1] == str(int(bk[1]) - 1))
#         and (wk[0] == bk[0])
#         and (wk[1] == str(int(bk[1]) + 1))
#     )
#     or (
#         (wr[1] == str(int(bk[1]) + 1))
#         and (wk[0] == bk[0])
#         and (wk[1] == str(int(bk[1]) - 1))
#     )
# )
# # Na ścianie
# checked_on_wall = (
#     ((bk[0] == "a") and (wr[0] == "a") and (bk[1] == wk[1]) and (wk[0] == "b"))
#     or ((bk[0] == "h") and (wr[0] == "h") and (bk[1] == wk[1]) and (wk[0] == "g"))
#     or ((bk[1] == "1") and (wr[1] == "1") and (bk[0] == wk[0]) and (wk[1] == "2"))
#     or ((bk[1] == "8") and (wr[1] == "8") and (bk[0] == wk[0]) and (wk[1] == "7"))
# )
# # W rogu
# checked_on_corner = (
#     ((bk == "a8") and (wr == "a7" and ((wk == "b7") or (wk == "b8"))))
#     or ((bk == "a8") and (wr == "b8" and ((wk == "a7") or (wk == "b7"))))
#     or ((bk == "a8") and (wr == "b7"))
#     or ((bk == "a1") and (wr == "a2" and ((wk == "b1") or (wk == "b2"))))
#     or ((bk == "a1") and (wr == "b1" and ((wk == "a2") or (wk == "b2"))))
#     or ((bk == "a1") and (wr == "b2"))
#     or ((bk == "h8") and (wr == "h7" and ((wk == "g7") or (wk == "g8"))))
#     or ((bk == "h8") and (wr == "g8" and ((wk == "h7") or (wk == "g7"))))
#     or ((bk == "h8") and (wr == "g7"))
#     or ((bk == "h1") and (wr == "h2" and ((wk == "g1") or (wk == "g2"))))
#     or ((bk == "h1") and (wr == "g1" and ((wk == "h2") or (wk == "g2"))))
#     or ((bk == "h1") and (wr == "g2"))
# )
# return checked or checked_on_wall or checked_on_corner
# Na ścianie
