def priority(char):
    x = ord(char)

    if ord('a') <= x <= ord('z'):
        return x - ord('a') + 1
    return x - ord('A') + 27

# Part I
res = 0

with open('p03.txt') as f:
    for l in f:
        first, second = l[:len(l) // 2], l[len(l) // 2:]
        common = set(first) & set(second)
        res += priority(next(iter(common)))

print(res)

# Part II
with open('p03.txt') as f:
    lines = f.readlines()

res, i = 0, 0

while True:
    try:
        one, two, three = lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()
    except IndexError:
        break
    common = set(one) & set(two) & set(three)
    tmp = priority(next(iter(common)))
    res += tmp
    i += 3

print(res)
