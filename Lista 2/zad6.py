import numpy as np
import queue

INADMISSABILITY = 1.5

class State:
    def __init__(self, positions, depth=0, path=""):
        self.positions = positions
        self.depth = depth
        self.path = path

    def __str__(self):
        return f'Positions:{self.positions}, depth:{self.depth}, path:{self.path}'

    def __hash__(self):
        N, M = lab.shape
        sum = 0
        for pos in self.positions:
            sum *= N * M
            sum = sum % 805306457
            sum += pos[0] * N + pos[1]
        return int(sum)

    def __eq__(self, other):
        return self.positions == other.positions

    def __lt__(self,other):
        return self.depth < other.depth

    def move_all(self, dir):
        list_of_pos = [move(pos, dir) for pos in self.positions]
        return State(set(list_of_pos), self.depth + 1, self.path + dir)

    def is_finished(self):
        for pos in self.positions:
            if lab[pos] not in ["G", "B"]:
                return False
        return True

    def dist(self):
        dist = 0
        for pos in self.positions:
            dist = max(dist, distances[pos])
        return INADMISSABILITY * dist


def move(pos, dir):
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


def count_distances():
    distances = np.zeros(lab.shape) + np.inf
    destinations = set(map(lambda x: tuple(x), np.argwhere((lab == "G") | (lab == "B"))))
    for destination in destinations:
        distances[destination] = 0
        queue = [destination]
        while queue:
            current_pos = queue.pop()
            for dir in moves:
                new_pos = move(current_pos, dir)
                if(lab[new_pos] != "#" and distances[current_pos] + 1 < distances[new_pos]):
                    distances[new_pos] = distances[current_pos] + 1
                    queue.append(new_pos)
    return distances


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
distances = count_distances()
q = queue.PriorityQueue()
q.put((starting_state.dist(), starting_state))
visited = set()
visited.add(starting_state)
while q:
    current_state = q.get()
    for dir in moves:
        new_state = current_state[1].move_all(dir)
        if new_state.is_finished():
            print(len(new_state.path))
            with open("./zad_output.txt", "w") as f:
                f.write(new_state.path)
            exit()
        if new_state not in visited:
            visited.add(new_state)
            q.put((new_state.depth + new_state.dist(), new_state))
