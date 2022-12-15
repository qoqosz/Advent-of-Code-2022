def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])
   
# Part I 
def find(S, B, y):
    d = dist(S, B)
    d_prime = abs(S[1] - y)
    res = set()
    
    if d > d_prime:
        for i in range(S[0], S[0] + d - d_prime + 1):
            res.add(i)
    if d >= d_prime:
        for i in range(S[0] - d + d_prime, S[0]):
            res.add(i)
            
    return res
    

data = []

with open('p15.txt') as f:
    for line in f:
        s, b = line.strip().split(':')
        s = s.replace('Sensor at ', '')
        b = b.replace('closest beacon is at ', '')
        s_xy, b_xy = s.split(','), b.split(',')

        sensor = tuple(int(p.split('=')[1]) for p in s_xy)
        beacon = tuple(int(p.split('=')[1]) for p in b_xy)

        data.append((sensor, beacon))
        
res = set()
target_y = 2_000_000
beacons_on_target = set(p[1][0] for p in data if p[1][1] == target_y)

for S, B in data:
    res |= find(S, B, target_y)
    
res -= beacons_on_target

print(len(res))

# Part II
data_w_dist = []

for S, B in data:
    data_w_dist.append((S, B, dist(S, B)))
    
    
def iter_circle(x0, d):
    visited = set()
    
    for i in range(d + 1):
        for s in (1, -1):
            for t in (1, -1):
                p = (x0[0] + t * (d - i), x0[1] + i * s)
        
                if not (0 <= p[0] <= 4_000_000 and 0 <= p[1] <= 4_000_000):
                    continue
        
                if p not in visited:
                    visited.add(p)
                    yield p


def is_beacon(X, data):
    for S, _, d in data:
        if dist(S, X) <= d:
            return False
            
    return True
    
    
for S, _, d in data_w_dist:    
    for x in iter_circle(S, d + 1):
        if is_beacon(x, data_w_dist):
            break

    else:
        continue
    break
    
print(x[0] * 4_000_000 + x[1])