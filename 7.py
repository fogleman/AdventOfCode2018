from collections import defaultdict
import fileinput
import re

tasks = set()
deps = defaultdict(set)
for line in fileinput.input():
    a, b = re.findall(r' ([A-Z]) ', line)
    tasks |= {a, b}
    deps[b].add(a)

# part 1
done = []
for _ in tasks:
    done.append(min(x for x in tasks
        if x not in done and deps[x] <= set(done)))
print(''.join(done))

# part 2
done = set()
seconds = 0
counts = [0] * 5
work = [''] * 5
while True:
    for i, count in enumerate(counts):
        if count == 1:
            done.add(work[i])
        counts[i] = max(0, count - 1)
    while 0 in counts:
        i = counts.index(0)
        candidates = [x for x in tasks if deps[x] <= done]
        if not candidates:
            break
        task = min(candidates)
        tasks.remove(task)
        counts[i] = ord(task) - ord('A') + 61
        work[i] = task
    if sum(counts) == 0:
        break
    seconds += 1
print(seconds)
