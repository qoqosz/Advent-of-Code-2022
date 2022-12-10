from dataclasses import dataclass

@dataclass
class Section:
    start: int
    end: int

    def __init__(self, start, end):
        assert start <= end
        self.start = start
        self.end = end

    def contains(self, other):
        return (self.start <= other.start) and (self.end >= other.end)
    
    def overlap(self, other):
        try:
            return Section(max(self.start, other.start), min(self.end, other.end))
        except AssertionError:
            return None
        
    @classmethod
    def from_str(cls, x):
        s, e = map(int, x.split('-'))
        return cls(s, e)


# Problem 1
count = 0

with open('p04.txt') as f:
    for line in f:
        sec1, sec2 = line.strip().split(',')
        sec1, sec2 = Section.from_str(sec1), Section.from_str(sec2)
        
        if sec1.contains(sec2) or sec2.contains(sec1):
            count += 1
            
print(count)

# Problem 2
count = 0

with open('p04.txt') as f:
    for line in f:
        sec1, sec2 = line.strip().split(',')
        sec1, sec2 = Section.from_str(sec1), Section.from_str(sec2)
        
        if sec1.overlap(sec2):
            count += 1
        
print(count)

