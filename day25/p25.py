DIGITS = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
INV_DIGITS = {v: k for k, v in DIGITS.items()}


def snafu2num(s):
    return sum(DIGITS[n] * 5 ** i
               for i, n in enumerate(s[::-1]))

def num2snafu(n):
    out = []

    while n:
        n, rem = divmod(n, 5)

        if rem <= 2:
            out.append(rem)
        else:
            out.append(rem - 5)
            n += 1

    return ''.join(str(INV_DIGITS[x]) for x in out[::-1])


with open('p25.txt') as f:
    nums = [n.strip() for n in f.readlines()]

print(num2snafu(sum(map(snafu2num, nums))))
