import fileinput

lines = list(fileinput.input())

def part1():
    return sum(map(int, lines))

def part2():
    f = 0
    seen = {f}
    while True:
        for line in lines:
            f += int(line)
            if f in seen:
                return f
            seen.add(f)

print(part1())
print(part2())
