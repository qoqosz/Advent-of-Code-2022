from itertools import cycle
import numpy as np


boundaries = 0b100000001
pieces = (  # flipped upside-down
            (0b000111100,),  # ####
    
            (0b000010000,    #  #
             0b000111000,    # ###
             0b000010000),   #  #
    
            (0b000111000,    # ###
             0b000001000,    #   #
             0b000001000),   #   #

            (0b000100000,    # # 
             0b000100000,    # #
             0b000100000,    # #
             0b000100000),   # #
    
            (0b000110000,    # ##
             0b000110000)    # ##
)

def push(block, jet):
    if jet == '<':
        return tuple(x << 1 for x in block)
    return tuple(x >> 1 for x in block)


def piece_repr(piece):
    if type(piece) == int:
        piece = tuple((piece,))
        
    return '\n'.join(format(x, '#011b') for x in piece)


class Tetris:
    def __init__(self, pieces, jet_pattern):
        self.jiter = iter(cycle(jet_pattern))
        self.piter = iter(cycle(pieces))
        self.h = 3
        self.board = {}
        
    def is_collision(self, h, piece):
        board_slice = tuple(self.board.get(i, boundaries) 
                            for i in range(h, h + len(piece)))
        
        return any(x & y for x, y in zip(board_slice, piece))

    def process(self):
        piece = next(self.piter)

        while True:
            jet = next(self.jiter)  # gas pushes rock
            shifted_piece = push(piece, jet)

            if not self.is_collision(self.h, shifted_piece):
                piece = shifted_piece    

            # check down movement
            if self.is_collision(self.h - 1, piece) or self.h == 0:
                # stop, add pieces to solids
                for i, j in enumerate(range(self.h, self.h + len(piece))):
                    self.board[j] = self.board.get(j, boundaries) | piece[i]

                self.h = max(self.board.keys()) + 4      
                break
            else:
                self.h -= 1  # moving down
                
    def board_repr(self, h_0, h):
        b = '\n'.join(piece_repr(self.board.get(i, boundaries)) 
                      for i in reversed(range(h_0, h_0 + h)))
            
        b += '\n'
        b = (b.replace('0b1', '|')
              .replace('1\n', '|\n')
              .replace('0', '.')
              .replace('1', '#'))
        
        return b
      
with open('p17.txt') as f:
    jet_pattern = f.read().strip()
    
      
# Part I
t = Tetris(pieces, jet_pattern)

for _ in range(2022):
    t.process()
    
print(t.h - 3)

# Part II

# First, simulate 50k rocks to record a pattern in the board
t = Tetris(pieces, jet_pattern)

for _ in range(50_000):
    t.process()
    
pattern = [t.board[i] for i in range(t.h - 3)]

# Then, start shifting a pattern and calculate the "cost".
# When cost is minimized, the cycle in the pattern and shifted
# one overlaps, which results in the minimal cost.
def find_min(pattern):
    min_cost = 1_000_000_000_000
    i_min = 0
    data = np.array(pattern)
    
    for i in range(1_000, 20_000):
        cost =  np.abs(data[i:] - data[:-i]).sum()
        
        if cost < min_cost:
            min_cost = cost
            i_min = i
            
    return i_min, min_cost

i_min, _ = find_min(pattern)
sub_pattern = pattern[i_min:i_min+40]

# Find indices of the sub_pattern in the pattern
def subfinder(mylist, pattern):
    matches = []
    for i in range(len(mylist)):
        if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
            matches.append(i)
    return matches
    
idx = np.array(subfinder(pattern, sub_pattern))

# Run a simulation again to get a number of rocks that have to fall
# in order to fill in the board up to a height of idx[0]
t = Tetris(pieces, jet_pattern)

for i in range(10_000):
    t.process()
    
    if (t.h - 3) > idx[0]:
        break
        
i_max = i

a, b = divmod(1000000000000, i_max)

# Again, run a simulation b times to record the height
t = Tetris(pieces, jet_pattern)

for i in range(b):
    t.process()
    
print(a * idx[0] + (t.h - 3))