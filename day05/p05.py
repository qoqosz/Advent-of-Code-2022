with open('p05.txt') as f:
    head = [next(f) for _ in range(8)]
    next(f)
    next(f)
    moves = [x for x in f]


def parse(move):
    return [int(x) for x in move.split() if x.isdigit()]


def get_stack(head):
    stack = [[] for _ in range(9)]

    for line in head:
        for i, char in enumerate(line):
            if char.isalpha():
                idx = (i - 1) // 4
                stack[idx].append(char)

    return [x[::-1] for x in stack]


def top_read(stack):
    return ''.join(s[-1] for s in stack)


# Part I
def do_move(stack, qty, src, dest):
    for _ in range(qty):
        item = stack[src - 1].pop()
        stack[dest - 1].append(item)


stack = get_stack(head)

for move in moves:
    do_move(stack, *parse(move))

print(top_read(stack))

# Part II 
def do_move2(stack, qty, src, dest):
    tmp = []

    for _ in range(qty):
        tmp.append(stack[src - 1].pop())

    for _ in range(qty):
        stack[dest - 1].append(tmp.pop())

stack = get_stack(head)

for move in moves:
    do_move2(stack, *parse(move))

print(top_read(stack))

