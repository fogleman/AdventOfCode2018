import fileinput

n = int(next(fileinput.input()))

def step(scores, i, j):
    s = scores[i] + scores[j]
    if s >= 10:
        scores.append(1)
    scores.append(s % 10)
    i = (i + scores[i] + 1) % len(scores)
    j = (j + scores[j] + 1) % len(scores)
    return (i, j)

# part 1
scores, i, j = [3, 7], 0, 1
while len(scores) < n + 10:
    i, j = step(scores, i, j)
print(''.join(map(str, scores[n:n+10])))

# part 2
scores, i, j = [3, 7], 0, 1
digits = list(map(int, str(n)))
while True:
    i, j = step(scores, i, j)
    if scores[-len(digits)-1:-1] == digits:
        print(len(scores) - len(digits) - 1)
        break
    if scores[-len(digits):] == digits:
        print(len(scores) - len(digits))
        break
