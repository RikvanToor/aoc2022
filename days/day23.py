import utils

def parse(input):
  return [list(l) for l in input.strip().split('\n')]

def norths(pos):
  x,y = pos
  return ([(x-1,y-1),(x,y-1),(x+1,y-1)], (x,y-1))

def easts(pos):
  x,y = pos
  return ([(x+1,y-1),(x+1,y),(x+1,y+1)], (x+1,y))

def souths(pos):
  x,y = pos
  return ([(x-1,y+1),(x,y+1),(x+1,y+1)], (x,y+1))

def wests(pos):
  x,y = pos
  return ([(x-1,y-1),(x-1,y),(x-1,y+1)], (x-1,y))

def sim(elves, n=None):
  dirs = [norths, souths, wests, easts]
  all_dirs = lambda p: [(x2,y2) for x2 in range(p[0]-1,p[0]+2) for y2 in range(p[1]-1,p[1]+2) if (p[0] != x2 or p[1] != y2)]
  dir_index = 0
  rounds = 0
  while True:
    rounds += 1
    targets = {}
    skip_counter = 0
    for e in elves:
      if all(map(lambda e2: e2 not in elves, all_dirs(e))):
        skip_counter += 1
        continue
      for i in range(4):
        di = (i + dir_index) % 4
        to_checks, target = dirs[di](e)
        if all(map(lambda e2: e2 not in elves, to_checks)):
          if target not in targets:
            targets[target] = [e]
          else:
            targets[target].append(e)
          break
    if skip_counter == len(elves):
      return elves, rounds

    for t in targets:
      es = targets[t]
      match es:
        case [e]:
          elves.remove(e)
          elves.add(t)
    dir_index += 1

    if rounds == n:
      return elves, rounds


def part_1(input):
  elves = {(x,y) for y, l in enumerate(input) for x,c in enumerate(l) if c == '#'}
  elves,_ = sim(elves, 10)
  min_x = min(map(lambda p: p[0], elves))
  max_x = max(map(lambda p: p[0], elves))
  min_y = min(map(lambda p: p[1], elves))
  max_y = max(map(lambda p: p[1], elves))
  return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)

def part_2(input):
  elves = {(x,y) for y, l in enumerate(input) for x,c in enumerate(l) if c == '#'}
  _,n = sim(elves)
  return n