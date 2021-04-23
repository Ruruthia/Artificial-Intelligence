import numpy as np

class State:
    def __init__(self, positions, depth=0, path=""):
        self.positions = positions
        self.depth = depth
        self.path = path

    def __hash__(self):
        N, M = lab.shape
        sum = 0
        for pos in self.positions:
            sum *= N * M
            sum += pos[0] * N + pos[1]
        return int(sum)

    def __eq__(self, other):
        return len(self.positions.symmetric_difference(other.positions)) == 0

    def move(self, pos, dir):
        new_pos = pos
        if dir == "U":
            if lab[(pos[0] - 1, pos[1])] != "#":
                new_pos = (pos[0] - 1, pos[1])
        elif dir == "D":
            if lab[(pos[0] + 1, pos[1])] != "#":
                new_pos = (pos[0] + 1, pos[1])
        elif dir == "L":
            if lab[(pos[0], pos[1] - 1)] != "#":
                new_pos = (pos[0], pos[1] - 1)
        elif dir == "R":
            if lab[(pos[0], pos[1] + 1)] != "#":
                new_pos = (pos[0], pos[1] + 1)
        return new_pos

    def move_all(self, dir, length):
        temp_set = set()
        for pos in self.positions:
            new_pos = pos
            for _ in range(length):
                new_pos = self.move(new_pos, dir)
            temp_set.add(new_pos)
        return State(temp_set, self.depth + length, self.path + length*dir)

    def is_finished(self):
        for pos in self.positions:
            if lab[pos] not in ["G", "B"]:
                return False
        return True

    def minimize_uncertainty(self, limit, desired_uncertainty):
        uncertainty = len(self.positions)
        state = self
        while len(state.path) <= limit:
            length = np.random.randint(1, 5)
            dir = moves[np.random.randint(4)]
            new_state = state.move_all(dir, length)
            if len(new_state.positions) < uncertainty or np.random.random() < 0.2:
                state = new_state
                uncertainty = len(state.positions)
            if uncertainty <= desired_uncertainty:
                return state, uncertainty
        return state, uncertainty


lab = []
moves = ["U", "D", "L", "R"]
lines = 0
with open("./zad_input.txt", "r") as f:
    for line in f:
        lab.append(list(line.strip()))
        lines += 1
lab = np.array(lab)
lab = lab.reshape(lines, -1)
starting_state = State(
    set(map(lambda x: tuple(x), np.argwhere((lab == "S") | (lab == "B"))))
)
desired_uncertainty = 2
while True:
    new_state, new_uncertainty = starting_state.minimize_uncertainty(80, desired_uncertainty)
    if len(new_state.positions) <= desired_uncertainty:
        starting_state = new_state
        break
assert(len(new_state.positions) <= desired_uncertainty)
queue = [starting_state]
visited = set()
visited.add(starting_state)
while queue:
    current_state = queue.pop(0)
    for dir in moves:
        new_state = current_state.move_all(dir, 1)
        if new_state.is_finished():
            print(new_state.depth)
            print(new_state.path)
            with open("./zad_output.txt", "w") as f:
                f.write(new_state.path)
            exit()
        if new_state not in visited:
            visited.add(new_state)
            queue.append(new_state)
