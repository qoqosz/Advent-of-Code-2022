import re


graph = {}
flow_rates = {}
pattern = r'(.*?)([A-Z]{2})(.*?)rate=(\d+)(.*?)valve(s)* (.*?)$'

with open('p16.txt') as f:
    for l in f:
        try:
            mg = re.match(pattern, l.strip()).groups()
        except AttributeError:
            print(l)
        flow_rates[mg[1]] = int(mg[3])
        graph[mg[1]] = [x.strip() for x in mg[-1].split(',')]
        

def iter_search(start, time=30):
    queue = [(start, 0, (), time)]
    visited = set()
    max_flow = 0
    
    for i in range(time):
        tmp = []
        
        for state in queue:
            if state in visited:
                continue
                
            visited.add(state)
            node, flow, opened, t = state
            
            if t < 0:
                continue
            
            # move
            for adj in graph[node]:
                tmp.append((adj, flow, opened, t - 1))           
            
            # open valve
            node_flow_rate = flow_rates[node]
            
            if node_flow_rate > 0 and node not in opened:
                opened = tuple(sorted(opened + (node,)))
                new_flow = flow + node_flow_rate * (t - 1)
                max_flow = max(max_flow, new_flow)
                tmp.append((node, new_flow, opened, t - 1))
            
            # do nothing
            tmp.append((node, flow, opened, t - 1))
            
        tmp = sorted(tmp, key=lambda x: x[1], reverse=True)[:6_000]
        queue = tmp
    
    return max_flow
    
    
print(iter_search('AA', 30))