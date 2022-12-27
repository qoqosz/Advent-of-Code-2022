from collections import Counter, deque


DIRECTIONS = {
    'N':  (-1,  0),
    'S':  ( 1,  0),
    'E':  ( 0,  1),
    'W':  ( 0, -1),
    'NE': (-1,  1),
    'NW': (-1, -1),
    'SE': ( 1,  1),
    'SW': ( 1, -1),
}
CHECKS = [
    (('N', 'NE', 'NW'), 'N'),
    (('S', 'SE', 'SW'), 'S'),
    (('W', 'NW', 'SW'), 'W'),
    (('E', 'NE', 'SE'), 'E')
]


def span(scan, axis=0):
    return (min(e[axis] for e in scan), max(e[axis] for e in scan))


def shape(scan):
    minh, maxh = span(scan)
    minw, maxw = span(scan, axis=1)

    return (maxh - minh + 1, maxw - minw + 1)


def pprint(scan):
    import numpy as np

    arr = np.full(shape(scan), '.')

    for pos in scan:
        arr[(pos[0] - minh, pos[1] - minw)] = '#'

    print('\n'.join(''.join(row) for row in arr))


def adj(pos):
    for v in DIRECTIONS.values():
        yield (pos[0] + v[0], pos[1] + v[1])


def mv(pos, d):
    return (pos[0] + d[0], pos[1] + d[1])


def proposals(elves_scan, shift=0):
    checks = deque(CHECKS)
    checks.rotate(-shift)
    props, stay = {}, set()
    # check elves in neighbourhood
    for elf in elves_scan:
        if any(e in elves_scan for e in adj(elf)):
            props[elf] = None
        else:
            stay.add(elf)

    # check directions of move
    for elf in props:
        for dirs, move in checks:
            if all(mv(elf, DIRECTIONS[d]) not in elves_scan for d in dirs):
                props[elf] = mv(elf, DIRECTIONS[move])
                break

    return props, stay


def eval_moves(proposals):
    cnt = Counter(proposals.values())
    moves, stay = {}, set()

    for k, v in proposals.items():
        if v is None:
            moves[k] = k
        elif cnt[v] == 1:
            moves[k] = v

    return moves


def eval_round(elves_scan, n=0):
    props, scan = proposals(elves_scan, n)
    moves = eval_moves(props)

    for k in props:
        if k not in moves:
            scan.add(k)

    for _, v in moves.items():
        scan.add(v)

    return scan

# Part I
def empty_ground(scan):
    w, h = shape(scan)
    return w * h - len(scan)


scan = set()

with open('p23.txt') as f:
    for i, line in enumerate(f.readlines()):
        for j, char in enumerate(line):
            if char == '#':
                scan.add((i, j))


scan1 = set(scan)

for i in range(10):
    scan1 = eval_round(scan1, i)

print(empty_ground(scan1))

# Part II
i = 0

while True:
    new_scan = eval_round(scan, i)

    if new_scan == scan:
        print(i + 1)
        break

    scan = new_scan
    i += 1
