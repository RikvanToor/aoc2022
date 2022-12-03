import utils

def parse(input):
  return [list(map(to_prio, l)) for l in input.strip().split('\n')]

def to_prio(c):
  if c >= 'a':
    return ord(c) - ord('a') + 1
  else:
    return ord(c) - ord('A') + 27

def halves(l):
  half_index = round(len(l)/2)
  return (l[0:half_index],l[half_index:])

def part_1(input):
  h = map(halves, input)
  res = [sum(set([x for x in h1 if x in h2])) for (h1, h2) in h]
  return sum(res)

def part_2(input):
  chunks = [input[i:i+3] for i in range(0, len(input), 3)]
  intersections = [sum(set([x for x in c1 if x in c2 if x in c3]))
                   for [c1, c2, c3] in chunks]
  return sum(intersections)