import fileinput
import re

class Model:
    def __init__(self, lines):
        self.clay = set()
        for line in lines:
            a, b0, b1 = map(int, re.findall(r'\d+', line))
            for b in range(b0, b1 + 1):
                self.clay.add((a, b) if line[0] == 'x' else (b, a))
        self.y0 = min(y for x, y in self.clay)
        self.y1 = max(y for x, y in self.clay)
        self.pile = set(self.clay)
        self.still = set()
        self.flowing = set()
    def run(self, x, y):
        self.queue = [(self.fall, x, y)]
        while self.queue:
            func, *args = self.queue.pop()
            func(*args)
    def fall(self, x, y):
        while y <= self.y1 and not (x, y + 1) in self.pile:
            self.flowing.add((x, y))
            y += 1
        if y <= self.y1:
            self.flowing.add((x, y))
            self.queue.append((self.scan, x, y))
    def scan(self, x, y):
        x0 = x1 = x
        while (x0, y + 1) in self.pile and not (x0 - 1, y) in self.clay:
            x0 -= 1
        while (x1, y + 1) in self.pile and not (x1 + 1, y) in self.clay:
            x1 += 1
        if (x0 - 1, y) in self.clay and (x1 + 1, y) in self.clay:
            for i in range(x0, x1 + 1):
                self.still.add((i, y))
                self.pile.add((i, y))
            self.queue.append((self.scan, x, y - 1))
        else:
            for i in range(x0, x1 + 1):
                self.flowing.add((i, y))
            if not (x0 - 1, y) in self.clay:
                self.queue.append((self.fall, x0, y))
            if not (x1 + 1, y) in self.clay:
                self.queue.append((self.fall, x1, y))

model = Model(fileinput.input())
model.run(500, 0)
print(sum(1 for x, y in model.still | model.flowing
    if y >= model.y0 and y <= model.y1))
print(sum(1 for x, y in model.still
    if y >= model.y0 and y <= model.y1))
