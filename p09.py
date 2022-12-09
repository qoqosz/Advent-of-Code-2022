motions = []

with open('p09.txt') as f:
    for l in f:
        d, m = l.strip().split(' ')
        motions.append((d, int(m)))

directions = {
    'D': 0 - 1j,
    'U': 0 + 1j,
    'L': -1,
    'R': 1,
    'DR': 1 - 1j,
    'DL': -1 -1j,
    'UR': 1 + 1j,
    'UL': -1 + 1j,
}

class Sim:
    def __init__(self):
        self.tvisited = set((0, 0))
        self.H = self.T = 0
        
    def dist2(self):
        d = self.H - self.T
        return d.real ** 2 + d.imag**2

    def tdir_hv(self):
        """Where T should move - in which horizontal / vertical dir?"""
        d = self.H - self.T
        
        if abs(d.real) > abs(d.imag):
            return 'R' if d.real > 0 else 'L'
        return 'U' if d.imag > 0 else 'D'

    def tdir_diag(self):
        """Where T should move - in which diagonal dir?"""
        d = self.H - self.T
        a = 'U' if d.imag > 0 else 'D'
        b = 'R' if d.real > 0 else 'L'
        return a + b
        
    def step(self, direction: str):
        self.move_head(direction)
        self.move_tail()
        
    def move_head(self, direction: str):
        self.H += directions[direction]
   
    def move_tail(self):        
        # horizontal or vertical move
        if abs(self.dist2() - 4) < 0.001:
            self.T += directions[self.tdir_hv()]
            self.tvisited.add((self.T.real, self.T.imag))
        # diagonal move
        elif abs(self.dist2() - 5) < 0.001:
            self.T += directions[self.tdir_diag()]
            self.tvisited.add((self.T.real, self.T.imag))
        # part 2 move
        elif abs(self.dist2()) > 8 - 0.001:
            self.T += directions[self.tdir_diag()]
            self.tvisited.add((self.T.real, self.T.imag))

# Part I
s = Sim()

for step in motions:
    d, n = step
    for _ in range(n):
        s.step(d)

print(len(s.tvisited))

# Part II
rope = [Sim() for _ in range(9)]

for step in motions:
    d, n = step
    for _ in range(n):
        rope[0].step(d)
        
        for k in range(1, 9):
            rope[k].H = rope[k - 1].T
            rope[k].move_tail()

print(len(rope[-1].tvisited))
