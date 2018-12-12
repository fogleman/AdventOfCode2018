import fileinput

lines = list(fileinput.input())
initial_state = set(i for i, x in
    enumerate(lines[0].split()[-1]) if x == '#')
rules = dict(line.split()[::2] for line in lines[2:])

def step(state):
    result = set()
    for i in range(min(state) - 2, max(state) + 3):
        w = ''.join('#' if j in state else '.'
            for j in range(i - 2, i + 3))
        if rules[w] == '#':
            result.add(i)
    return result

# part 1
s = initial_state
for i in range(20):
    s = step(s)
print(sum(s))

# part 2
s = initial_state
p = n = 0
for i in range(1000):
    p = n
    s = step(s)
    n = sum(s)
print(p + (n - p) * (50000000000 - i))
