import utils

def parse(input):
  return [[(int(r.split('-')[0]), int(r.split('-')[1])) for r in l.split(',')]
          for l in input.strip().split('\n')]

def part_1(input):
  counter = 0
  for [(p1_min, p1_max), (p2_min, p2_max)] in input:
    if (p1_min <= p2_min and p1_max >= p2_max) or (p2_min <= p1_min and p2_max >= p1_max):
      counter += 1
  return counter

def part_2(input):
  counter = 0
  for [(p1_min, p1_max), (p2_min, p2_max)] in input:
    if (p1_min <= p2_min and p1_max >= p2_min) or (p2_min <= p1_min and p2_max >= p1_min):
      counter += 1
  return counter