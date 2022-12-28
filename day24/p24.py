import numpy as np


class Valley:
    motions = '><v^'
    moves = ((1, 1), (-1, 1), (1, 0), (-1, 0))  # (offset, axis)

    def __init__(self, basin):
        self.blizzards = self._blizzards(basin)
        self.blizzards_next = self.next()
        self.shape = basin.shape
        self.t = 0
        self.start = (-1, 0)
        self.end = (self.shape[0], self.shape[1] - 1)

    def adj(self, pos):
        poss = [(pos[0] + dt[0], pos[1] + dt[1])
                for dt in ((1, 0), (-1, 0), (0, 1), (0, -1))]

        yield pos

        for p in poss:
            if p in (self.start, self.end):
                yield p
            elif (0 <= p[0] < self.shape[0]) and (0 <= p[1] < self.shape[1]):
                yield p

    def _blizzards(self, basin):
        return {
            w: np.where(basin == ord(w), True, False)
            for w in self.motions
        }

    def next(self):
        return {
            w: np.roll(bliz, *move)
            for (w, bliz), move in zip(self.blizzards.items(), self.moves)
        }

    def process(self):
        """Move blizzards."""
        self.t += 1
        self.blizzards = self.next()
        self.blizzards_next = self.next()
        return self

    def __repr__(self):
        summed = sum(self.blizzards.values())
        res = np.zeros_like(summed)

        for m in self.motions:
            blizz = self.blizzards[m]

            res[(summed < 2) & blizz] = ord(m)

        res[summed > 1] = ord('X')
        res[summed == 0] = ord('.')

        return (f't = {self.t}\n'
                + '\n'.join(''.join(chr(c) for c in line)
                            for line in res))


def bfs(valley, start, end):
    queue = set((start,))

    while True:
        next_blizz = sum(valley.blizzards_next.values())
        _queue = set()

        for pos in queue:
            for n in valley.adj(pos):
                if n == end:
                    valley.process()
                    return valley.t

                if n not in (start, end):
                    if next_blizz[n] != 0:
                        continue

                _queue.add(n)

        valley.process()
        queue = _queue

    return None


# Part I
with open('p24.txt') as f:
    basin = f.read()
    w = basin.index('\n')
    h = basin.count('\n')
    arr = np.frombuffer(basin.replace('\n', '').encode(), dtype='u1')
    arr = arr.reshape((h, w))
    arr = arr[1:-1, 1:-1]


val = Valley(arr)
t1 = bfs(val, start=val.start, end=val.end)
print(t1)

# Part II
_ = bfs(val, start=val.end, end=val.start)
t2 = bfs(val, start=val.start, end=val.end)
print(t2)
