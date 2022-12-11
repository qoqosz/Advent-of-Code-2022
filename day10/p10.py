class CPU:
    def __init__(self):
        self.X = 1
        self.cycle = 0
        
    def state(self):
        """Representation of CPU state."""
        return self.cycle, self.X
    
    def step(self):
        """Increase a cycle by 1."""
        self.cycle += 1
        return self.state()
        
    def noop(self):
        """Execute `noop` instruction."""
        yield self.step()
        
    def addx(self, x):
        """Excecute `addx x` instruction."""
        yield self.step()
        yield self.step()   
        self.X += x
        
    def iter(self, instructions):
        """
        Execute a list of instructions and iterate 
        over its intermediate states.
        """
        for i in instructions:
            if i == 'noop':
                yield from self.noop()
            else:
                x = int(i.split(' ')[1])
                yield from self.addx(x)
                


instructions = []

with open('p10.txt') as f:
    for l in f:
        instructions.append(l.strip())

# Part I
cycles = [20, 60, 100, 140, 180, 220]
print(sum(cycle * value 
          for cycle, value in CPU().iter(instructions) 
          if cycle in cycles))
          
# Part II
def wrap(text, width=40):
    return '\n'.join(text[i:i + width] 
                     for i in range(0, len(text), width))
                     
idx_crt = 0
display = ''

for cycle, value in CPU().iter(instructions):
    # display chars changed for better readability
    if abs(idx_crt - value) <= 1:
        display += '█'
    else:
        display += ' '
    
    idx_crt = (idx_crt + 1) % 40
    

print(wrap(display))
