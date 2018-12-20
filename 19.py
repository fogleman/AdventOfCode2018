import fileinput
import re

instructions = {
    'addr': lambda r, a, b: r[a] + r[b],
    'addi': lambda r, a, b: r[a] + b,
    'mulr': lambda r, a, b: r[a] * r[b],
    'muli': lambda r, a, b: r[a] * b,
    'banr': lambda r, a, b: r[a] & r[b],
    'bani': lambda r, a, b: r[a] & b,
    'borr': lambda r, a, b: r[a] | r[b],
    'bori': lambda r, a, b: r[a] | b,
    'setr': lambda r, a, b: r[a],
    'seti': lambda r, a, b: a,
    'gtir': lambda r, a, b: int(a > r[b]),
    'gtri': lambda r, a, b: int(r[a] > b),
    'gtrr': lambda r, a, b: int(r[a] > r[b]),
    'eqir': lambda r, a, b: int(a == r[b]),
    'eqri': lambda r, a, b: int(r[a] == b),
    'eqrr': lambda r, a, b: int(r[a] == r[b]),
}

def load_program(lines):
    program = []
    for line in lines:
        if line.startswith('#ip'):
            ip_register = int(line.split()[-1])
            continue
        f = instructions[line.split()[0]]
        a, b, c = map(int, re.findall(r'\d+', line))
        program.append((f, a, b, c))
    return ip_register, program

def run_program(ip_register, program, registers, max_cycles=0):
    ip = 0
    cycles = 0
    while ip >= 0 and ip < len(program):
        registers[ip_register] = ip
        f, a, b, c = program[ip]
        registers[c] = f(registers, a, b)
        ip = registers[ip_register] + 1
        cycles += 1
        if max_cycles and cycles >= max_cycles:
            break
    return registers

ip_register, program = load_program(fileinput.input())

# part 1
registers = [0, 0, 0, 0, 0, 0]
print(run_program(ip_register, program, registers)[0])

# part 2
registers = [1, 0, 0, 0, 0, 0]
n = max(run_program(ip_register, program, registers, 1000))
total = 0
for i in range(1, n + 1):
    if n % i == 0:
        total += i
print(total)
