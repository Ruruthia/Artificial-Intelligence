def opt_dist(block, D):
    block = list(map(int, list(block)))
    switch = 0
    start = 0
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


with open("zad4_input.txt", "r") as f_in:
    with open("zad4_output.txt", "w") as f_out:
        for line in f_in:
            test = line.split(" ")
            f_out.write(str(opt_dist(test[0], int(test[1]))) + "\n")
