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
}

def sign(x):
    if x == 0:
        return 0
    return -1 if x < 0 else 1

class SimRope:
    def __init__(self):
        self.t_visited = set((0, 0))
        self.H = self.T = 0
        
    def step(self, direction: str):
        self.move_head(direction)
        self.move_tail()
        
    def move_head(self, direction: str):
        self.H += directions[direction]
   
    def move_tail(self): 
        delta = self.H - self.T
        
        if abs(delta) > 1.5:
            self.T += sign(delta.real) + sign(delta.imag) * 1j
            self.t_visited.add((self.T.real, self.T.imag))

            
def sim_rope(motions, n_knots=2):
    rope = [SimRope() for _ in range(n_knots - 1)]
    
    for step in motions:
        d, n = step
        
        for _ in range(n):
            rope[0].step(d)
            
            for k in range(1, n_knots - 1):
                rope[k].H = rope[k - 1].T
                rope[k].move_tail()
                
    return len(rope[-1].t_visited)
            
# Part I
print(sim_rope(motions))

# Part I
print(sim_rope(motions, 10))