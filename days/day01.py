import utils

def parse(input):
  groups = list(map(lambda xs: map(int, xs.split()), input.split('\n\n')))
  return groups

def part_1(input):
  return max(map(sum, input))

def part_2(input):
  top = sorted(list(map(sum, input)), reverse=True)
  return sum(top[0:3])