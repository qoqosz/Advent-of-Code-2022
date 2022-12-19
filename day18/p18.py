from collections import deque


def neighbors3d(p):
    for i in (-1, 1):
        yield (p[0] + i, p[1], p[2])
        yield (p[0], p[1] + i, p[2])
        yield (p[0], p[1], p[2] + i)
        
# Part I
def count_faces(data):
    n_total = 0
    
    for p in data:
        for n in neighbors3d(p):
            if n in data:
                n_total += 1
    
    return len(data) * 6 - n_total
    

data = set()

with open('p18.txt') as f:
    for l in f:
        row = l.strip().split(',')
        row = tuple(int(x) for x in row)
        data.add(row)
        
print(count_faces(data))

# Part II
def lava_fill(data):
    """
    Fill in the grid with lava and count with how many faces 
    it will touch.
    """
    visited = set((0, 0, 0))
    queue = deque([(0, 0, 0)])
    n_faces = 0
    
    while queue:
        node = queue.popleft()
        
        for w in neighbors3d(node):           
            if any(not (-1 <= x <= 20) for x in w):
                continue
            
            if w in data:
                # lava touches an exposed face
                n_faces += 1
            else:
                if w not in visited:
                    visited.add(w)
                    queue.append(w)

    return n_faces

print(lava_fill(data))
