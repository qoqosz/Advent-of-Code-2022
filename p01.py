calories, tmp = [], []

with open('p01.txt') as f:
    for line in f:
        try:
            num = int(line)
            tmp.append(num)
        except ValueError:
            calories.append(tmp)
            tmp = []

print(max(map(sum, calories)))
print(sum(sorted(map(sum, calories), reverse=True)[:3]))            
