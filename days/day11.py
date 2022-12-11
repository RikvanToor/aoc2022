import utils
import re
import math

class Monkey:
  def __init__(self, items, operation, division_factor, true_target, false_target):
    self.items = items
    self.operation = operation
    self.division_factor = division_factor
    self.true_target = true_target
    self.false_target = false_target
    self.inspection_counter = 0
  
  def get_target(self, value):
    if value % self.division_factor == 0:
      return self.true_target
    return self.false_target

  def run(self, monkeys, div_by_three):
    total_factor = math.prod([m.division_factor for m in monkeys])
    for i in self.items:
      self.inspection_counter += 1
      new_value = self.operation(i)
      if div_by_three:
        new_value //= 3
      new_value %= total_factor
      target = self.get_target(new_value)
      monkeys[target].items.append(new_value)
    self.items = []

def parse_monkey(input):
  i = input.split('\n')
  p = re.compile('\d+')
  starting_items = [int(x) for x in p.findall(i[1])]
  division_factor = int(p.findall(i[3])[0])
  true_target = int(p.findall(i[4])[0])
  false_target = int(p.findall(i[5])[0])
  # This is VERY dangerous, but whatever :-)
  operation = eval('lambda old: ' + i[2][19:])

  return Monkey(starting_items, operation, division_factor, true_target, false_target)

def parse(input):
  ms = input.rstrip().split('\n\n')
  monkeys = [parse_monkey(m) for m in ms]
  return monkeys

def get_result(monkeys):
  inspections = [m.inspection_counter for m in monkeys]
  inspections.sort()
  return math.prod(inspections[-2:])

def part_1(input):
  for r in range(20):
    for m in input:
      m.run(input, True)
  return(get_result(input))

def part_2(input):
  for r in range(10000):
    for m in input:
      m.run(input, False)
  return(get_result(input))
