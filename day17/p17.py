from itertools import cycle


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