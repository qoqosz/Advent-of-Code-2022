rules = {
    'A': {'X': 0, 'Y': 1, 'Z': -1},
    'B': {'X': -1, 'Y': 0, 'Z': 1},
    'C': {'X': 1, 'Y': -1, 'Z': 0}
}
shape_score = {'A': 1, 'B': 2, 'C': 3, 
               'X': 1, 'Y': 2, 'Z': 3}
outcome_score = {-1: 0, 0: 3, 1: 6}
score = 0
shapes = []

with open('p02.txt') as f:
    for l in f:
        a, b = l.strip().split(' ')
        shapes.append((a, b))
        score += outcome_score[rules[a][b]] + shape_score[b]

# Part I
print(score)

# Part II
outcome = {'X': -1, 'Y': 0, 'Z': 1}
score = 0

for a, b in shapes:
    res = outcome[b]
    bprime = {v: k for k, v in rules[a].items()}[res]
    score += outcome_score[res] + shape_score[bprime]

print(score)
