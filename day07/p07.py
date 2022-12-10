from functools import cache

class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = []
        self.dirs = {}
        self.get = self.dirs.get
        
    def __repr__(self):
        return f'Dir({self.name})'
    
    @cache
    def size(self):
        return sum(f for f in self.files) + sum(d.size() for _, d in self.dirs.items())
    
    def add_dir(self, name):
        self.dirs[name] = Dir(name, parent=self)
        
    def add_file(self, name, size):
        self.files.append(size)
        

with open('p07.txt') as f:
    cmds = f.read().split('\n')
    

root = Dir('/')
cwd = root

for cmd in cmds[1:]:
    cmd = cmd.strip()
    
    if not cmd:
        break
        
    if cmd.startswith('$'):
        if 'cd' in cmd:
            name = cmd[5:]
            
            if name == '..':
                cwd = cwd.parent
            else:
                cwd = cwd.get(name)
                
        elif 'ls' in cmd:
            continue
    elif cmd.startswith('dir'):
        name = cmd[4:]
        cwd.add_dir(name)
    else:
        size, _ = cmd.split(' ')
        cwd.add_file(None, int(size))


# Part I
max_size = 100_000
sum_total = 0

def check_dir(directory):
    global sum_total
    
    if directory.size() <= max_size:
        sum_total += directory.size()
        
    for sub_dir in directory.dirs.values():
        check_dir(sub_dir)
        
check_dir(root)
print(sum_total)

# Part II
total_disk_space = 70_000_000
required_space = 30_000_000
sizes = []

def get_size(directory):
    global sizes
    
    sizes.append(directory.size())
         
    for sub_dir in directory.dirs.values():
        get_size(sub_dir)

get_size(root)
free_space = total_disk_space - root.size()
to_be_freed = required_space - free_space
print(min(x for x in sizes if x >= to_be_freed))
