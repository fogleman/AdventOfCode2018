import fileinput

n = int(next(fileinput.input()))

def step(scores, current):
    s = scores[current[0]] + scores[current[1]]
    if s >= 10:
        scores.append(1)
    scores.append(s % 10)
    current[0] = (current[0] + scores[current[0]] + 1) % len(scores)
    current[1] = (current[1] + scores[current[1]] + 1) % len(scores)

# part 1
scores, current = [3, 7], [0, 1]
while len(scores) < n + 10:
    step(scores, current)
print(''.join(map(str, scores[n:n+10])))

# part 2
scores, current = [3, 7], [0, 1]
digits = list(map(int, str(n)))
num_digits = len(digits)
while True:
    step(scores, current)
    if scores[-num_digits-1:-1] == digits:
        print(len(scores) - num_digits - 1)
        break
    if scores[-num_digits:] == digits:
        print(len(scores) - num_digits)
        break
