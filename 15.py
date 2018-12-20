from itertools import count
import fileinput
import heapq

def shortest_paths(source, targets, occupied):
    result = []
    best = None
    visited = set(occupied)
    queue = [(0, [source])]
    while queue:
        distance, path = heapq.heappop(queue)
        if best and len(path) > best:
            return result
        node = path[-1]
        if node in targets:
            result.append(path)
            best = len(path)
            continue
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adjacent({node}):
            if neighbor in visited:
                continue
            heapq.heappush(queue, (distance + 1, path + [neighbor]))
    return result

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def adjacent(positions):
    return set((y + dy, x + dx)
        for y, x in positions
            for dy, dx in [(-1, 0), (0, -1), (0, 1), (1, 0)])

def choose_target(position, targets, occupied):
    if not targets:
        return None
    if position in targets:
        return position
    paths = shortest_paths(position, targets, occupied)
    ends = [x[-1] for x in paths]
    return min(ends) if ends else None

def choose_move(position, target, occupied):
    if position == target:
        return position
    paths = shortest_paths(position, {target}, occupied)
    starts = [x[1] for x in paths]
    return min(starts) if starts else None

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
    def run(self):
        while True:
            if not self.step():
                return self.rounds, self.total_hp()
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

lines = list(fileinput.input())

# part 1
rounds, hp = Model(lines).run()
print(rounds * hp)

# part 2
for elf_attack in count(4):
    try:
        rounds, hp = Model(lines, elf_attack).run()
        print(rounds * hp)
        break
    except Exception:
        pass
