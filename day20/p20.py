def modif(line):
    # input can have duplicated values
    data = [(i, val) for i, val in enumerate(line)]
    orig = list(data)
    n = len(line)
    
    for i, val in orig:
        idx = data.index((i, val))
        data.pop(idx)
        # (n - 1) because we popped one elemenet
        data.insert((idx + val) % (n - 1), (i, val))
        
    return [x[1] for x in data]
    
def score(data):
    indices = [1000, 2000, 3000]
    n = len(data)
    return sum(data[(data.index(0) + i) % n] for i in indices)
    
# Part I
with open('p20.txt') as f:
    line = [int(x) for x in f.readlines()]
    
print(score(modif(line)))

# Part II
decryption_key = 811589153
line = [decryption_key * x for x in line]

def modif2(line, t=10):
    # input can have duplicated values
    data = [(i, val) for i, val in enumerate(line)]
    orig = list(data)
    n = len(line)
    
    for _ in range(t):
        for i, val in orig:
            idx = data.index((i, val))
            data.pop(idx)
            # (n - 1) because we popped one elemenet
            data.insert((idx + val) % (n - 1), (i, val))
        
    return [x[1] for x in data]
    
print(score(modif2(line)))