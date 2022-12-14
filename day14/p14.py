from collections import namedtuple
from operator import or_
from functools import reduce


class Point(namedtuple('Point', 'x y')):
    def __iadd__(self, other):
        self = self.__add__(other)
        return self
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    @classmethod
    def from_str(self, p):
        return Point(*[int(x) for x in p.split(',')])
        
        
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
        if start.x == end.x:
            self.type = 'v'
        elif start.y == end.y:
            self.type = 'h'
        else:
            raise ValueError(f'Invalid line: {start} - {end}')
            
    def __contains__(self, point):
        if self.type == 'v':
            return point.x == self.start.x and self.miny <= point.y <= self.maxy
        else:
            return point.y == self.start.y and self.minx <= point.x <= self.maxx
        
    @property
    def minx(self):
        return min(self.start.x, self.end.x)
    
    @property
    def maxx(self):
        return max(self.start.x, self.end.x)
    
    @property
    def miny(self):
        return min(self.start.y, self.end.y)
    
    @property
    def maxy(self):
        return max(self.start.y, self.end.y)
    
    def to_set(self):
        if self.type == 'h':
            return set((x, self.start.y) for x in range(self.minx, self.maxx + 1))
        else:
            return set((self.start.x, y) for y in range(self.miny, self.maxy + 1))
            
            
class Path:
    def __init__(self, points):
        self.lines = []
        
        for i in range(1, len(points)):
            self.lines.append(Line(points[i - 1], points[i]))
            
    def __contains__(self, point):
        return any(point in line for line in self.lines)
    
    def to_set(self):
        return reduce(or_, (line.to_set() for line in self.lines))   
        
        
class Cave:
    def __init__(self, paths, max_depth=10):
        self.rocks = reduce(or_, (path.to_set() for path in paths))
        self.sand = set()
        self.max_depth = max_depth
        self.prev = None
        
    def is_air(self, point):
        return not (point in self.rocks or point in self.sand)

    
    def pour(self, src):
        """assume same source"""
        if not self.prev:
            return self._pour(src)
        
        if self.is_air(self.prev):
            return self._pour(self.prev)
        
        self.prev = self.prev - Point(0, 1)
        
        if self.prev != src:
            return self._pour(self.prev)
        
        raise ValueError('Cave filled in!')    
    
    def _pour(self, src):
        prev = None
        
        while True:
            if src.y >= self.max_depth:
                raise StopIteration('Point falling out into the deep')            
            
            dts = [Point(0, 1), Point(-1, 1), Point(1, 1)]
            move_on = False
            
            for dt in dts:
                dest = src + dt
                
                if self.is_air(dest):
                    prev = src
                    src += dt
                    move_on = True
                    break
                    
            if move_on:
                continue
              
            self.sand.add(src)
            self.prev = prev
            break
                
        return src    
        
        
sand = Point(500, 0)

with open('p14.txt') as f:
    paths = []
    
    for l in f:
        path = Path([Point.from_str(p) for p in l.strip().split(' -> ')])
        paths.append(path)
        

# Part I
cave = Cave(paths, max_depth=200)
i = 0

while True:
    try:
        cave.pour(sand)
    except StopIteration:
        print(i)
        break
    i += 1      
    
# Part II
def highest_y(paths):
    max_depth = 0
    
    for path in paths:
        for line in path.lines:
            max_depth = max(max_depth, line.maxy)
            
    return max_depth
    
floor_y = 2 + highest_y(paths)
floor = Path([Point(-100_000, floor_y), Point(100_000, floor_y)])
cave = Cave([*paths, floor], max_depth=floor_y)
i = 0

while True:
    try:
        dest = cave.pour(sand)
        
        if dest == sand:
            print(i+1)
            break
    except StopIteration:
        print(i)
        break
    i += 1
