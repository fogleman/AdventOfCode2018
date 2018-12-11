from collections import defaultdict
import fileinput

def summed_area_table(n):
    t = defaultdict(int)
    for y in range(1, 301):
        for x in range(1, 301):
            r = x + 10
            p = (((r * y + n) * r) // 100) % 10 - 5
            t[(x, y)] = p + t[(x, y - 1)] + t[(x - 1, y)] - t[(x - 1, y - 1)]
    return t

def region_sum(t, s, x, y):
    x0, y0, x1, y1 = x - 1, y - 1, x + s - 1, y + s - 1
    return t[(x0, y0)] + t[(x1, y1)] - t[(x1, y0)] - t[(x0, y1)]

def best(t, s):
    rs = []
    for y in range(1, 301 - s + 1):
        for x in range(1, 301 - s + 1):
            r = region_sum(t, s, x, y)
            rs.append((r, x, y))
    return max(rs)

t = summed_area_table(int(next(fileinput.input())))
print('%d,%d' % best(t, 3)[1:])
print('%d,%d,%d' % max(best(t, s) + (s,) for s in range(1, 301))[1:])
