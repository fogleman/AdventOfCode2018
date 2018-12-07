from collections import defaultdict
import fileinput
import re

points = [tuple(map(int, re.findall(r'\d+', x))) for x in fileinput.input()]

x0, x1 = min(x for x, y in points), max(x for x, y in points)
y0, y1 = min(y for x, y in points), max(y for x, y in points)

def dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# part 1
counts = defaultdict(int)
infinite = set()
for y in range(y0, y1 + 1):
    for x in range(x0, x1 + 1):
        ds = sorted((dist(x, y, px, py), i)
            for i, (px, py) in enumerate(points))
        if ds[0][0] != ds[1][0]:
            counts[ds[0][1]] += 1
            if x == x0 or y == y0 or x == x1 or y == y1:
                infinite.add(ds[0][1])
for k in infinite:
    counts.pop(k)
print(max(counts.values()))

# part 2
count = 0
for y in range(y0, y1 + 1):
    for x in range(x0, x1 + 1):
        if sum(dist(x, y, px, py) for px, py in points) < 10000:
            count += 1
print(count)
