def opt_dist(block, D):
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
    print(min)


opt_dist(list(map(int, list("0010001000"))), 5)
opt_dist(list(map(int, list("0010001000"))), 4)
opt_dist(list(map(int, list("0010001000"))), 3)
opt_dist(list(map(int, list("0010001000"))), 2)
opt_dist(list(map(int, list("0010001000"))), 1)
opt_dist(list(map(int, list("0010001000"))), 0)
