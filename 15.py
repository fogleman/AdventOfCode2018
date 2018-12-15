from itertools import count
import fileinput
import heapq

DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def shortest_path(source, target, occupied):
    visited = set()
    queue = [(0, 0, [source])]
    while queue:
        _, distance, path = heapq.heappop(queue)
        node = path[-1]
        if node == target:
            return path
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adjacent({node}):
            if neighbor in occupied:
                continue
            if neighbor in visited:
                continue
            new_path = list(path)
            new_path.append(neighbor)
            new_distance = distance + 1
            estimated_distance = manhattan_distance(neighbor, target)
            new_score = new_distance + estimated_distance
            heapq.heappush(queue, (new_score, new_distance, new_path))

def manhattan_distance(a, b):
    ay, ax = a
    by, bx = b
    return abs(ax - bx) + abs(ay - by)

def adjacent(positions):
    return set((y + dy, x + dx) for y, x in positions for dy, dx in DIRS)

def choose_target(position, targets, occupied):
    if position in targets:
        return position
    results = []
    for target in targets:
        path = shortest_path(position, target, occupied)
        if path:
            results.append((len(path), path[-1]))
    return min(results)[-1] if results else None

def choose_move(position, target, occupied):
    if position == target:
        return position
    results = []
    for neighbor in adjacent({position}) - occupied:
        path = shortest_path(neighbor, target, occupied)
        if path:
            results.append((len(path), path[0]))
    return min(results)[-1]

class Unit:
    def __init__(self, team, position):
        self.team = team
        self.position = position
        self.hp = 200

class Model:
    def __init__(self, lines, elf_attack=None):
        self.elf_attack = elf_attack
        self.walls = set()
        self.units = []
        self.rounds = 0
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip()):
                if c == '#':
                    self.walls.add((y, x))
                elif c in 'EG':
                    self.units.append(Unit(c, (y, x)))
    def total_hp(self):
        return sum(x.hp for x in self.units if x.hp > 0)
    def occupied(self, unit=None):
        units = set(x.position for x in self.units
            if x != unit and x.hp > 0)
        return self.walls | units
    def get_move(self, unit):
        occupied = self.occupied(unit)
        targets = set(x.position for x in self.units
            if x.team != unit.team and x.hp > 0)
        if not targets:
            return None
        in_range = adjacent(targets) - occupied
        target = choose_target(unit.position, in_range, occupied)
        if target is None:
            return unit.position
        move = choose_move(unit.position, target, occupied)
        return move
    def get_attack(self, unit):
        units = [(x.hp, x.position, x) for x in self.units
            if x.team != unit.team and x.hp > 0 and
                manhattan_distance(unit.position, x.position) == 1]
        return min(units)[-1] if units else None
    def step(self):
        units = sorted(self.units, key=lambda x: x.position)
        for unit in units:
            if unit.hp <= 0:
                continue
            move = self.get_move(unit)
            if move is None:
                return False
            unit.position = move
            attack = self.get_attack(unit)
            if attack:
                if self.elf_attack:
                    if unit.team == 'G':
                        attack.hp -= 3
                        if attack.hp <= 0:
                            raise Exception
                    else:
                        attack.hp -= self.elf_attack
                else:
                    attack.hp -= 3
        self.rounds += 1
        return True
    def __str__(self):
        units = dict((x.position, x) for x in self.units if x.hp > 0)
        x0 = min(x for y, x in self.walls)
        x1 = max(x for y, x in self.walls)
        y0 = min(y for y, x in self.walls)
        y1 = max(y for y, x in self.walls)
        rows = []
        for y in range(y0, y1 + 1):
            row = []
            row_units = []
            for x in range(x0, x1 + 1):
                c = '#' if (y, x) in self.walls else '.'
                unit = units.get((y, x))
                if unit:
                    c = unit.team
                    row_units.append(unit)
                row.append(c)
            row.append('   ')
            row.append(', '.join('%s(%d)' % (unit.team, unit.hp)
                for unit in row_units))
            rows.append(''.join(row))
        return '\n'.join(rows) + '\n'

# part 1
lines = list(fileinput.input())
model = Model(lines)
while True:
    if not model.step():
        break
print(model.rounds * model.total_hp())

# part 2
for elf_attack in count(4):
    try:
        model = Model(lines, elf_attack)
        while True:
            if not model.step():
                break
        print(model.rounds * model.total_hp())
        break
    except Exception:
        pass
