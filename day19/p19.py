import re
import numpy as np
from collections import deque

with open('p19.txt') as f:
    blueprints = [list(map(int, re.findall('\d+', line))) for line in f]
    
# blueprint list:
# blueprint_id, ore_robot_ore, clay_robot_ore, obsidian_robot_ore, obsidian_robot_clay, geode_robot_ore, geode_robot_obsidian

# state tuple:
# ore, clay, obsidina, geode, ore_robot, clay_robot, obsidian_robot, geode_robot, time

def bfs(state0, blueprint, max_time=24):
    _, o_r_o, c_r_o, ob_r_o, ob_r_c, g_r_o, g_r_ob = blueprint
    queue = deque([state0])
    visited = set()
    max_geodes = 0
    
    while queue:
        s = queue.popleft()
        
        if s in visited:
            continue
            
        visited.add(s)
        o, c, ob, g, o_r, c_r, ob_r, g_r, t = s
        
        if g > max_geodes:
            max_geodes = g
            
        if t == max_time:
            continue
            
        # build ore robot
        if o >= o_r_o and o <= 3 * o_r_o:
            queue.append((o - o_r_o + o_r,
                          c + c_r,
                          ob + ob_r,
                          g + g_r,
                          o_r + 1,
                          c_r,
                          ob_r,
                          g_r,
                          t + 1))
        # build clay robot
        if o >= c_r_o and o <= 3 * c_r_o:
            queue.append((o - c_r_o + o_r,
                          c + c_r,
                          ob + ob_r,
                          g + g_r,
                          o_r,
                          c_r + 1,
                          ob_r,
                          g_r,
                          t + 1))
        # build obsidian robot
        if o >= ob_r_o and c >= ob_r_c and o <= 3 * ob_r_o and c <= 3 * ob_r_c:
            queue.append((o - ob_r_o + o_r,
                          c - ob_r_c + c_r,
                          ob + ob_r,
                          g + g_r,
                          o_r,
                          c_r,
                          ob_r + 1,
                          g_r,
                          t + 1))
        # build geode robot
        if o >= g_r_o and ob >= g_r_ob and o <= 3 * g_r_o and ob <= 3 * g_r_ob:
            queue.append((o - g_r_o + o_r,
                          c + c_r,
                          ob - g_r_ob + ob_r,
                          g + g_r,
                          o_r,
                          c_r,
                          ob_r,
                          g_r + 1,
                          t + 1))
        # don't build robots
        queue.append((o + o_r,
                      c + c_r,
                      ob + ob_r,
                      g + g_r,
                      o_r,
                      c_r,
                      ob_r,
                      g_r,
                      t + 1))
    
    return max_geodes
    
# Part I
state0 = (0, 0, 0, 0, 1, 0, 0, 0, 0)

result = 0

for blueprint in blueprints:
    max_geodes = bfs(state0, blueprint)
    quality_level = max_geodes * blueprint[0]
    result += quality_level
    
print(result)

# Part II
# Reworked approach

# Nice shorthand for creating arrays
arr = lambda *x: np.array(x)

with open('p19.txt') as f:
    blueprints = [list(map(int, re.findall('\d+', line))) for line in f]
    
# Convert blueprint to the following format:
# `i, ((resources to build a robot_i, robot spec_i), ..., (resources to build a robot_N, robot spec_N))`
def parse(blueprint):
    i, a, b, c, d, e, f = blueprint
    
    return (i, ((arr(0, f, 0, e), arr(1, 0, 0, 0)),   # build geode robot
                (arr(0, 0, d, c), arr(0, 1, 0, 0)),   # obsidian
                (arr(0, 0, 0, b), arr(0, 0, 1, 0)),   # clay
                (arr(0, 0, 0, a), arr(0, 0, 0, 1)),   # ore
                (arr(0, 0, 0, 0), arr(0, 0, 0, 0))))  # no build  
                
def search(blueprint, max_time=24):
    resources = arr(0, 0, 0, 0)
    robots = arr(0, 0, 0, 1)
    queue = [(resources, robots)]
    
    for t in range(max_time):
        tmp = []
        for resources, robots in queue:
            for cost, outcome in blueprint:
                # build a robot if we have enough resources
                if all(resources >= cost):
                    tmp.append((resources - cost + robots, robots + outcome))
        # sort by current resources + what will be produced
        # top 6000 is a heuristic
        queue = sorted(tmp, key=lambda x: tuple(x[0] + x[1]), reverse=True)[:6000]
    
    return queue[0][0][0]
    
result = 1

for bp in blueprints[:3]:
    i, blueprint = parse(bp)
    result *= search(blueprint, max_time=32)
    
print(result)