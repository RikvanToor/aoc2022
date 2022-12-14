import utils
from itertools import pairwise

def parse_line(l):
  cs = l.split(' -> ')
  return [(int(c.split(',')[0]), int(c.split(',')[1])) for c in cs]

def parse(input):
  ls = input.rstrip().split('\n')
  return [parse_line(l) for l in ls]

def create_rock_set(input):
  res = set()
  lowest_point = 0
  for p in input:
    for ((x1,y1),(x2,y2)) in pairwise(p):
      for x in range(min(x1,x2), max(x1,x2)+1):
        for y in range(min(y1,y2), max(y1,y2)+1):
          res.add((x,y))
          if y > lowest_point:
            lowest_point = y
  return res, lowest_point

def add_sand(rock_set, lowest_point, has_floor):
  sx,sy = (500,0)
  while True:
    if sy == lowest_point + 1 and has_floor:
      return sx,sy
    elif sy > lowest_point:
      return None
    elif (sx,sy+1) not in rock_set:
      sy += 1
    elif (sx-1,sy+1) not in rock_set:
      sx -= 1
      sy += 1
    elif (sx+1,sy+1) not in rock_set:
      sx += 1
      sy += 1
    else:
      return sx,sy

def part_1(input):
  rock_set,lowest_point = create_rock_set(input)
  counter = 0
  while True:
    match add_sand(rock_set, lowest_point, False):
      case None:
        return counter
      case sx,sy:
        rock_set.add((sx,sy))
    counter += 1

def part_2(input):
  rock_set,lowest_point = create_rock_set(input)
  counter = 0
  while True:
    match add_sand(rock_set, lowest_point, True):
      case 500,0:
        return counter+1
      case sx,sy:
        rock_set.add((sx,sy))
    counter += 1