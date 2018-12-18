from collections import deque
import cairocffi as cairo
import fileinput
import re

dirt = cairo.ImageSurface.create_from_png('tiles/12/dirt.png')
grass = cairo.ImageSurface.create_from_png('tiles/12/grass.png')
stone = cairo.ImageSurface.create_from_png('tiles/12/stone.png')
water = cairo.ImageSurface.create_from_png('tiles/12/water.png')
water_high = cairo.ImageSurface.create_from_png('tiles/12/water-high.png')
water_low = cairo.ImageSurface.create_from_png('tiles/12/water-low.png')

class Model:
    def __init__(self, lines):
        self.clay = set()
        self.still = set()
        self.flowing = set()
        self.still_t = {}
        self.flowing_t = {}
        for line in lines:
            a, b0, b1 = map(int, re.findall(r'\d+', line))
            for b in range(b0, b1 + 1):
                self.clay.add((a, b) if line[0] == 'x' else (b, a))
        self.x0 = min(x for x, y in self.clay)
        self.x1 = max(x for x, y in self.clay)
        self.y0 = min(y for x, y in self.clay)
        self.y1 = max(y for x, y in self.clay)
        self.queue = deque()
        self.seen = set()

    def run(self, x, y):
        self.queue.append((self.fall, x, y, 0))
        while self.queue:
            print(len(self.queue))
            x = self.queue.popleft()
            if x in self.seen:
                continue
            self.seen.add(x)
            func, *args = x
            func(*args)

    def count_all(self):
        return sum(1 for x, y in self.still | self.flowing
            if y >= self.y0 and y <= self.y1)

    def count_still(self):
        return sum(1 for x, y in self.still
            if y >= self.y0 and y <= self.y1)

    def stop(self, x, y):
        return (x, y) in self.clay

    def pile(self, x, y):
        return (x, y) in self.clay or (x, y) in self.still

    def add_flowing(self, x, y, t):
        self.flowing_t.setdefault((x, y), t)
        if t < self.flowing_t[(x, y)]:
            self.flowing_t[(x, y)] = t
        self.flowing.add((x, y))

    def add_still(self, x, y, t):
        self.still_t.setdefault((x, y), t)
        if t < self.still_t[(x, y)]:
            self.still_t[(x, y)] = t
        self.still.add((x, y))

    def fall(self, x, y, t):
        while y <= self.y1 and not self.pile(x, y + 1):
            self.add_flowing(x, y, t)
            t += 1
            y += 1
        if y <= self.y1:
            self.add_flowing(x, y, t)
            self.queue.append((self.scan, x, y, t))

    def scan(self, x, y, t):
        x0 = x
        while self.pile(x0, y + 1) and not self.stop(x0 - 1, y):
            x0 -= 1
        x1 = x
        while self.pile(x1, y + 1) and not self.stop(x1 + 1, y):
            x1 += 1
        stop0 = self.stop(x0 - 1, y)
        stop1 = self.stop(x1 + 1, y)
        nt = max(t + abs(i - x) for i in range(x0, x1 + 1))
        if stop0 and stop1:
            for i in range(x0, x1 + 1):
                self.add_still(i, y, t + abs(i - x))
            self.queue.append((self.scan, x, y - 1, nt))
        else:
            for i in range(x0, x1 + 1):
                self.add_flowing(i, y, t + abs(i - x))
            if not stop0:
                self.queue.append((self.fall, x0, y, t + abs(x0 - x)))
            if not stop1:
                self.queue.append((self.fall, x1, y, t + abs(x1 - x)))

    def __str__(self):
        x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1
        rows = []
        for y in range(y0, y1 + 1):
            row = []
            for x in range(x0, x1 + 1):
                c = '.'
                if (x, y) in self.clay:
                    c = '#'
                if (x, y) in self.flowing:
                    c = '|'
                if (x, y) in self.still:
                    c = '~'
                row.append(c)
            rows.append(''.join(row))
        return '\n'.join(rows)

    def render(self, t):
        scale = 1
        tile_size = 12
        still = set(k for k, v in self.still_t.items() if v <= t)
        flowing = set(k for k, v in self.flowing_t.items() if v <= t)
        wet = still | flowing
        maxy = max(y for x, y in wet)
        y0 = maxy - 56
        y1 = y0 + 112
        p = 0
        # x0, y0, x1, y1 = self.x0-p, self.y0-p, self.x1+p, self.y1+p
        x0, x1 = self.x0 - p, self.x1 + p
        w = int((x1 - x0 + 1) * tile_size * scale)
        h = int((y1 - y0 + 1) * tile_size * scale)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        dc = cairo.Context(surface)
        dc.scale(scale)
        
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px = (x - x0) * tile_size
                py = (y - y0) * tile_size
                dc.set_source_surface(stone, px, py)
                dc.paint()
                tile = None
                if (x, y) in self.clay:
                    tile = dirt
                    if (x, y - 1) not in self.clay:
                        tile = grass
                if (x, y) in wet:
                    if (x, y - 1) not in wet:
                        tile = water_high
                    else:
                        tile = water
                if tile:
                    dc.set_source_surface(tile, px, py)
                    dc.paint()
                if (x, y) in flowing and (x, y) not in still:
                    dc.set_source_surface(water_high, px, py)
                    dc.paint()
        return surface

model = Model(fileinput.input())
model.run(500, 0)
print(model.count_all())
print(model.count_still())

maxt = max(max(model.flowing_t.values()), max(model.still_t.values()))
for t in range(maxt + 1):
    print(t, maxt)
    surface = model.render(t)
    surface.write_to_png('out%06d.png' % t)
