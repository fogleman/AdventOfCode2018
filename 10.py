from itertools import count
import fileinput
import re

points = [tuple(map(int, re.findall(r'[-\d]+', x)))
    for x in fileinput.input()]

def state(points, t):
    return [(x + vx * t, y + vy * t) for x, y, vx, vy in points]

def bounds(points):
    x0, x1 = min(p[0] for p in points), max(p[0] for p in points)
    y0, y1 = min(p[1] for p in points), max(p[1] for p in points)
    return (x0, y0, x1, y1)

def area(points):
    x0, y0, x1, y1 = bounds(points)
    return (x1 - x0 + 1) * (y1 - y0 + 1)

def min_area_t(points):
    prev = area(points)
    for t in count():
        a = area(state(points, t))
        if a > prev:
            return t - 1
        prev = a

def display(points):
    x0, y0, x1, y1 = bounds(points)
    points = set(points)
    rows = []
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            row.append('*' if (x, y) in points else ' ')
        rows.append(''.join(row))
    return '\n'.join(rows)

t = min_area_t(points)
print(display(state(points, t)))
print(t)
