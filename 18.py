from collections import Counter
from itertools import count
import fileinput

lines = [line.strip() for line in fileinput.input()]

def make_grid(lines):
    grid = {}
    w, h = len(lines[0]), len(lines)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y)] = c
    return w, h, grid

def step(w, h, grid):
    result = {}
    for y in range(h):
        for x in range(w):
            c = grid[(x, y)]
            neighbors = [grid.get((x + dx, y + dy), '')
                for dy in range(-1, 2) for dx in range(-1, 2) if dy or dx]
            counts = Counter(neighbors)
            if c == '.':
                # An open acre will become filled with trees if three or more
                # adjacent acres contained trees. Otherwise, nothing happens.
                if counts['|'] >= 3:
                    c = '|'
            elif c == '|':
                # An acre filled with trees will become a lumberyard if three
                # or more adjacent acres were lumberyards. Otherwise, nothing
                # happens.
                if counts['#'] >= 3:
                    c = '#'
            elif c == '#':
                # An acre containing a lumberyard will remain a lumberyard if
                # it was adjacent to at least one other lumberyard and at least
                # one acre containing trees. Otherwise, it becomes open.
                if counts['#'] == 0 or counts['|'] == 0:
                    c = '.'
            result[(x, y)] = c
    return result

def resource_value(grid):
    counts = Counter(grid.values())
    return counts['|'] * counts['#']

# part 1
w, h, grid = make_grid(lines)
for i in range(10):
    grid = step(w, h, grid)
print(resource_value(grid))

# part 2
w, h, grid = make_grid(lines)
seen = {}
prev = 0
for i in count(1):
    grid = step(w, h, grid)
    v = resource_value(grid)
    cycle = i - seen.get(v, 0)
    if cycle == prev:
        if 1000000000 % cycle == i % cycle:
            print(resource_value(grid))
            break
    seen[v] = i
    prev = cycle
