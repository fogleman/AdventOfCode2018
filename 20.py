import fileinput
import ply.lex as lex
import ply.yacc as yacc

dirs = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

# lexer rules
tokens = ['LPAREN', 'RPAREN', 'OR', 'DIR']

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_OR = r'\|'
t_DIR = r'[NESW]+'

# parser rules
def p_pattern(t):
    'pattern : concat'
    t[0] = t[1]

def p_pattern_or(t):
    'pattern : pattern OR concat'
    t[0] = ('or', t[1], t[3])

def p_concat(t):
    'concat : term'
    t[0] = t[1]

def p_concat_term(t):
    'concat : concat term'
    t[0] = ('concat', t[1], t[2])

def p_term(t):
    'term : DIR'
    t[0] = ('dir', t[1])

def p_term_empty(t):
    'term :'
    t[0] = ('dir', '')

def p_term_paren(t):
    'term : LPAREN pattern RPAREN'
    t[0] = t[2]

# build lexer and parser given above rules
lexer = lex.lex(errorlog=lex.NullLogger())
parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())

def parse(text):
    text = text.strip().replace('^', '').replace('$', '')
    return parser.parse(text, lexer=lexer)

def visit(node, doors, points):
    if node[0] == 'concat':
        points = visit(node[1], doors, points)
        points = visit(node[2], doors, points)
        return points
    elif node[0] == 'or':
        a = visit(node[1], doors, points)
        b = visit(node[2], doors, points)
        return list(set(a) | set(b))
    else: # dir
        for d in node[1]:
            dx, dy = dirs[d]
            doors |= set((x, y, x + dx, y + dy) for x, y in points)
            doors |= set((x + dx, y + dy, x, y) for x, y in points)
            points = [(x + dx, y + dy) for x, y in points]
        return points

def locate_doors(text):
    doors = set()
    visit(parse(text), doors, [(0, 0)])
    return doors

def search(doors):
    distances = {}
    queue = [(0, 0, 0)]
    while queue:
        x, y, d = queue.pop()
        if (x, y) in distances and distances.get((x, y)) <= d:
            continue
        distances[(x, y)] = d
        for dx, dy in dirs.values():
            if (x, y, x + dx, y + dy) in doors:
                queue.append((x + dx, y + dy, d + 1))
    return distances

def show(doors):
    x0, x1 = min(d[0] for d in doors), max(d[0] for d in doors)
    y0, y1 = min(d[1] for d in doors), max(d[1] for d in doors)
    rows = ['#' * ((x1 - x0 + 1) * 2 + 1)]
    for y in range(y0, y1 + 1):
        row1, row2 = ['#'], ['#']
        for x in range(x0 , x1 + 1):
            has_door = any((x, y, x + dx, y + dy) in doors
                for dx, dy in dirs.values())
            c = '.' if has_door else '#'
            row1.append('X' if x == 0 and y == 0 else c)
            row1.append('.' if (x, y, x + 1, y) in doors else '#')
            row2.append('.#' if (x, y, x, y + 1) in doors else '##')
        rows.append(''.join(row1))
        rows.append(''.join(row2))
    return '\n'.join(rows)

doors = locate_doors(next(fileinput.input()))
# print(show(doors))
distances = search(doors)
print(max(distances.values()))
print(sum(x >= 1000 for x in distances.values()))
