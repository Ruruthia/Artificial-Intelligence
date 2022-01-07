import sys


def B(i, j):
    return "B_%d_%d" % (i, j)


def domains(Bs):
    return [b + " in 0..1" for b in Bs]


def get_col(j, R):
    return [B(i, j) for i in range(R)]


def get_row(i, C):
    return [B(i, j) for j in range(C)]


def col_sum(j, cols, R):
    return " + ".join(get_col(j, R)) + " #= " + str(cols[j])


def row_sum(i, rows, C):
    return " + ".join(get_row(i, C)) + " #= " + str(rows[i])


def correct_sums(R, rows, C, cols):
    correct_cols = [col_sum(j, cols, R) for j in range(C)]
    correct_rows = [row_sum(i, rows, C) for i in range(R)]
    return correct_cols + correct_rows


def one_in_three_R(R, C):
    cs = []
    for i in range(R):
        for j in range(C - 2):
            cs.append(
                B(i, j + 1) + " #= 1 #==> " + B(i, j) + " + " + B(i, j + 2) + " #> 0"
            )
    return cs


def one_in_three_C(R, C):
    cs = []
    for i in range(R - 2):
        for j in range(C):
            cs.append(
                B(i + 1, j) + " #= 1 #==> " + B(i, j) + " + " + B(i + 2, j) + " #> 0"
            )
    return cs


def one_in_three(R, C):
    return one_in_three_R(R, C) + one_in_three_C(R, C)


def two_in_four(R, C):
    cs = []
    for i in range(R - 1):
        for j in range(C - 1):
            cs.append(
                B(i, j)
                + " + "
                + B(i + 1, j + 1)
                + " #= 2 #<==> "
                + B(i + 1, j)
                + " + "
                + B(i, j + 1)
                + " #= 2"
            )
    return cs


def known_storms(triples):
    cs = []
    for i, j, val in triples:
        cs.append("%s #= %d" % (B(i, j), val))
    return cs


def print_constraints(Cs, indent, d):
    position = indent
    print(indent * " ", end="")
    for c in Cs:
        print(c + ",", end=" ")
        position += len(c)
        if position > d:
            position = indent
            print()
            print(indent * " ", end="")


def storms(rows, cols, triples):
    R = len(rows)
    C = len(cols)
    bs = [B(i, j) for i in range(R) for j in range(C)]
    sys.stdout = open("zad_output.txt", "w")
    print(":- use_module(library(clpfd)).")
    print("solve([" + ", ".join(bs) + "]) :- ")

    cs = (
        known_storms(triples)
        + domains(bs)
        + correct_sums(R, rows, C, cols)
        + one_in_three(R, C)
        + two_in_four(R, C)
    )
    print_constraints(cs, 4, 70)
    print()
    print("    labeling([ff], [" + ", ".join(bs) + "]).")
    print()
    print(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")
    sys.stdout.close()


txt = open("zad_input.txt").readlines()

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(list(map(int, txt[i].split())))

storms(rows, cols, triples)
