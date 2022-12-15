from ast import literal_eval


def compare(left, right):
    n_left, n_right = len(left), len(right)
    n = max(n_left, n_right)
    
    for i in range(n):
        # If the left list runs out of items first, the inputs are in the right order.
        if i >= n_left:
            return True
        # If the right list runs out of items first, the inputs are not in the right order.
        if i >= n_right:
            return False
        
        # If the lists are the same length and no comparison makes a decision about the order, 
        # continue checking the next part of the input.
        
        left_v, right_v = left[i], right[i]

        # If both values are integers, the lower integer should come first.
        if isinstance(left_v, int) and isinstance(right_v, int):
            if left_v < right_v:
                return True
            if left_v > right_v:
                return False
        else:
            # convert one element to a list
            if isinstance(left_v, int) and isinstance(right_v, list):
                left_v = [left_v]
            if isinstance(left_v, list) and isinstance(right_v, int):
                right_v = [right_v]

            res = compare(left_v, right_v)
            
            if res is not None:
                return res
    
# Part I
with open('p13.txt') as f:
    lines = f.readlines()

right_order = []

i = 0
while i < len(lines):
    a, b = lines[i].strip(), lines[i + 1].strip()
    a, b = literal_eval(a), literal_eval(b)

    if compare(a, b):
        right_order.append(i // 3 + 1)
    
    i += 3
    
print(sum(right_order))

# Part II
eval_lines = [[[2]], [[6]]]

for l in lines:
    l = l.strip()
    
    if l:
        eval_lines.append(literal_eval(l))

def bubble_sort(a):
    n = len(a)
    swapped = False
    
    while True:
        newn = 0
        
        for i in range(1, n):
            if not compare(a[i-1], a[i]):
                a[i-1], a[i] = a[i], a[i-1]
                newn = i
        n = newn
        
        if n <= 1:
            break
                
    return a
    
sorted_list = bubble_sort(eval_lines)
print((sorted_list.index([[2]]) + 1) * (sorted_list.index([[6]]) + 1))

def cmp(left, right):
    """
    Different approach with match statement pattern matching.
    
    Does not return anything if left and right are the same.
    """
    match left, right:
        case int(), int():
            if left < right:
                return True
            if left > right:
                return False
        case list(), int():
            return cmp(left, [right])
        case int(), list():
            return cmp([left], right)
        case list(), list():
            for a, b in zip(left, right):
                if (res := cmp(a, b)) is not None:
                    return res

            if len(left) < len(right):
                return True
            if len(left) > len(right):
                return False
                
res = sorted(eval_lines, key=cmp_to_key(lambda x, y: -int(cmp(x, y))))