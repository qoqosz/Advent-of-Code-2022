import re
import math

from collections import deque
from functools import cache


DEBUG = False


class Monkey:
    """Model each monkey as a singleton."""

    gang = {}

    @staticmethod
    @cache
    def lcm():
        return math.lcm(*[m.divisor for m in Monkey.gang.values()])

    def __new__(cls, no, relief_factor=3):
        if no in cls.gang:
            return cls.gang[no]
        else:
            self = super().__new__(cls)
            cls.gang[no] = self
            self.no = no
            self.n_inspects = 0
            self.relief_factor = relief_factor
            return self

    def inspect(self):
        while self.items:
            self._inspect(self.items.popleft())

    def _inspect(self, item):
        self.n_inspects += 1

        if DEBUG:
            print(f'  Monkey inspects an item with a worry level of {item}.')

        new = self.operation(item)

        if DEBUG:
            print(f'    New worry level is: {new}')

        new = (new // self.relief_factor) % Monkey.lcm()

        if DEBUG:
            print(f'    Monkey gets bored with item. Worry level is divided by 3 to {new}')

        i = self.test_item(new)

        if DEBUG:
            print(f'    Item with worry level {new} is thrown to monkey {i}')

        Monkey(i).items.append(new)


    def operation(self, old):
        return eval(self.op, dict(old=old))

    def test_item(self, val):
        return self.if_true if val % self.divisor == 0 else self.if_false


def round():
    for _, monkey in Monkey.gang.items():
        monkey.inspect()

def print_inventory():
    for _, monkey in Monkey.gang.items():
        print(monkey.items)

def monkey_business():
    vals = [m.n_inspects for m in Monkey.gang.values()]
    a, b = sorted(vals)[-2:]

    return a * b


with open('p11.txt') as f:
    text = [line.strip('\n') for line in f.read().split('\n')]

# Part I
for i in range(len(text)):
    if text[i].startswith('Monkey'):
        id_ = re.search('Monkey (\d+):', text[i]).group(1)
        monkey = Monkey(int(id_))
        monkey.items = deque(map(int, re.findall('(\d+)', text[i + 1])))
        monkey.op = text[i + 2][19:]
        monkey.divisor = int(text[i + 3][21:])
        monkey.if_true = int(text[i + 4][29:])
        monkey.if_false = int(text[i + 5][30:])
        i += 7

for _ in range(20):
    round()

print(monkey_business())

# Part II
Monkey.gang = {}

for i in range(len(text)):
    if text[i].startswith('Monkey'):
        id_ = re.search('Monkey (\d+):', text[i]).group(1)
        monkey = Monkey(int(id_), relief_factor=1)
        monkey.items = deque(map(int, re.findall('(\d+)', text[i + 1])))
        monkey.op = text[i + 2][19:]
        monkey.divisor = int(text[i + 3][21:])
        monkey.if_true = int(text[i + 4][29:])
        monkey.if_false = int(text[i + 5][30:])
        i += 7

for _ in range(10_000):
    round()

print(monkey_business())
