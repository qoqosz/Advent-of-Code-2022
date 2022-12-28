"""
               4-> 1->
             5         2
             |         |
             v         v
                    3->
             6     3
             |     |
             v     v
         6->
        ^          ^
        |          |
        5          2
               7->
        4    7
        |    |
        v    v
         1->    
"""
import re
import numpy as np


cube = {}

with open('p22.txt') as f:
    for i, line in enumerate(f, 1):
        for j, c in enumerate(line.strip('\n'), 1):
            if c in '.#':
                cube[(i, j)] = c
        if i == 202:
            break
    
    moves_list = re.findall(r'R|L|\d+', line)
    
    
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def solve(cube, moves_list, wrappings):
    idx_d = 0
    pos = (1, 51)

    for m in moves_list:
        if m == 'R':
            idx_d = (idx_d + 1) % 4
        elif m == 'L':
            idx_d = (idx_d - 1) % 4
        else:
            for _ in range(int(m)):
                dd = directions[idx_d]
                dest = (pos[0] + dd[0], pos[1] + dd[1])
            
                if dest not in cube:
                    dest, dd = wrappings[dest]
                
                if cube[dest] == '.':
                    pos = dest
                    idx_d = directions.index(dd)
                
    return 1000 * pos[0] + 4 * pos[1] + idx_d

# Part I
wrappings = {}

for i in range(1, 51):
    wrappings[(0, 100 + i)] = ((50, 100 + i), (-1, 0))  # 1->3
    wrappings[(51, 100 + i)] = ((1, 100 + i), (1, 0))   # 3->1
    
    wrappings[(i, 151)] = ((i, 51), (0, 1))             # 2->5
    wrappings[(i, 50)] = ((i, 150), (0, -1))            # 5->2
    
    wrappings[(0, 50 + i)] = ((150, 50 + i), (-1, 0))   # 4->7
    wrappings[(151, 50 + i)] = ((1, 50 + i), (1, 0))    # 7->4
    
    wrappings[(50 + i, 101)] = ((50 + i, 51), (0, 1))   # 3->6
    wrappings[(50 + i, 50)] = ((50 + i, 100), (0, -1))  # 6->3
    
    wrappings[(100 + i, 101)] = ((100 + i, 1), (0, 1))  # 2->5
    wrappings[(100 + i, 0)] = ((100 + i, 100), (0, -1)) # 5->2
    
    wrappings[(150 + i, 51)] = ((150 + i, 1), (0, 1))   # 7->4
    wrappings[(150 + i, 0)] = ((150 + i, 50), (0, -1))  # 4->7
    
    wrappings[(100, i)] = ((200, i), (-1, 0))           # 6->4
    wrappings[(201, i)] = ((101, i), (1, 0))            # 4->6
    
print(solve(cube, moves_list, wrappings))

# Part II
wrappings = {}

for i in range(1, 51):
    wrappings[(0, 100 + i)] = ((200, i), (-1, 0))  # 1
    wrappings[(201, i)] = ((1, 100 + i), (1, 0))   # inv 1
    
    wrappings[(i, 151)] = ((151 - i, 100), (0, -1))  # 2
    wrappings[(151 - i, 101)] = ((i, 150), (0, -1))  # inv 2
    
    wrappings[(51, 100 + i)] = ((50 + i, 100), (0, -1))  # 3
    wrappings[(50 + i, 101)] = ((50, 100 + i), (-1, 0))  # inv 3
    
    wrappings[(0, 50 + i)] = ((150 + i, 1), (0, 1))  # 4
    wrappings[(150 + i, 0)] = ((1, 50 + i), (1, 0))  # inv 4
    
    wrappings[(i, 50)] = ((151 - i, 1), (0, 1))  # 5
    wrappings[(151 - i, 0)] = ((i, 51), (0, 1))  # inv 5
    
    wrappings[(50 + i, 50)] = ((101, i), (1, 0)) # 6
    wrappings[(100, i)] = ((50 + i, 51), (0, 1)) # inv 6
    
    wrappings[(151, 50 + i)] = ((150 + i, 50), (0, -1)) # 7
    wrappings[(150 + i, 51)] = ((150, 50 + i), (-1, 0)) # inv 7
    
print(solve(cube, moves_list, wrappings))
