import numpy as np

with open('p08.txt') as f:
    trees = np.array([[int(x) for x in l.strip()] for l in f])

# Part I
def _is_visible_slice(slice_, pos, height):
    return (slice_[:pos] < height).all() or (slice_[pos + 1:] < height).all()

def is_visible(trees, pos):
    r, c = pos
    height = trees[pos]
    
    is_vis_row = _is_visible_slice(trees[r], c, height)
    is_vis_col = _is_visible_slice(trees[:, c], r, height)
    
    return is_vis_row | is_vis_col

def count_visible(trees):
    nrows, ncols = trees.shape
    count = 0
    
    for i in range(1, nrows - 1):
        for j in range(1, ncols - 1):
            count += int(is_visible(trees, (i, j)))
            
    return count + 2 * (nrows + ncols - 2)

print(count_visible(trees))

# Part II
def _score_left(row, pos, height):
    score = 1
    while score <= pos:
        if row[pos - score] >= height:
            break
        if score < pos:
            score += 1
        else:
            break
    
    return score

def _score_right(row, pos, height):
    score = 1
    n = len(row)
    while score + pos <= n - 1:
        if row[pos + score] >= height:
            break
        if score + pos < n - 1:
            score += 1
        else:
            break
    
    return score

def _score_up(col, pos, height):
    return _score_left(col, pos, height)

def _score_down(col, pos, height):
    return _score_right(col, pos, height)

def scenic_score(trees, pos):
    r, c = pos
    height = trees[pos]
    
    return (_score_up(trees[:, c], r, height)
            * _score_left(trees[r], c, height)
            * _score_down(trees[:, c], r, height)
            * _score_right(trees[r], c, height))

def max_scenix_score(trees):
    max_score = 0
    nrows, ncols = trees.shape
    
    for i in range(1, nrows - 1):
        for j in range(1, ncols - 1):
            score = scenic_score(trees, (i, j))
            
            if score > max_score:
                max_score = score
                
    return max_score

print(max_scenix_score(trees))
