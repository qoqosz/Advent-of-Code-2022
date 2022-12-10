def window(it, sz):
    tmp = []

    for i, elem in enumerate(it):
        if i < sz:
            tmp.append(elem)
            continue
        yield tmp
        tmp = tmp[1:] + [elem]

    if len(tmp) == sz:
        yield tmp


def idx_start(stream, sz=4):
    for i, w in enumerate(window(stream, sz)):
        if len(w) == len(set(w)):
            return i + sz


with open('p06.txt') as f:
    stream = f.read().strip()

# Part I
print(idx_start(stream))

# Part II
print(idx_start(stream, 14))
