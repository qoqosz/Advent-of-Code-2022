import numpy as np
from scipy.optimize import minimize


def eval_monkey(node):
    val = monkeys[node]
    
    if isinstance(val, (int, np.ndarray)):
        return val
    
    m1, op, m2 = val
    
    if op == '+':
        return eval_monkey(m1) + eval_monkey(m2)
    elif op == '-':
        return eval_monkey(m1) - eval_monkey(m2)
    elif op == '*':
        return eval_monkey(m1) * eval_monkey(m2)
    elif op == '/':
        return eval_monkey(m1) / eval_monkey(m2)
        

monkeys = {}

with open('p21.txt') as f:
    for line in f:
        monkey, op = line.strip().split(':')

        try:
            val = int(op)
            monkeys[monkey] = val
        except:
            monkeys[monkey] = op.strip().split(' ')
            
# Part I
print(int(eval_monkey('root')))

# Part II
m1, _, m2 = monkeys['root']

def eval_humn(num=726):
    global monkeys
    monkeys['humn'] = num
    return (eval_monkey(m1), eval_monkey(m2))
    
def cost(num):
    a, b = eval_humn(num)
    return (a - b) ** 2
    
res = minimize(cost, 700, method='Powell')
print(int(res.x))
