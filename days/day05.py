import utils
import re

def parse(input):
  (stacks_txt, proc) = input.rstrip().split('\n\n')
  stacks_lines = stacks_txt.split('\n')
  nr_stacks = int(stacks_lines[-1].split()[-1])
  stacks = [[] for _ in range(nr_stacks)]
  for l in reversed(stacks_lines[0:-1]):
    for i in range(nr_stacks):
      index = (i + 1) * 4 - 3
      if len(l) >= index:
        c = l[index]
        if c != ' ':
          stacks[i].append(c)

  p = re.compile('\d+')
  moves = [list(map(int, p.findall(l))) for l in proc.split('\n')]

  return (stacks, moves)

def part_1(input):
  (stacks, moves) = input
  for [quantity, fr, to] in moves:
    for i in range(quantity):
      c = stacks[fr-1].pop()
      stacks[to-1].append(c)

  return ''.join([s[-1] for s in stacks])

def part_2(input):
  (stacks, moves) = input
  for [quantity, fr, to] in moves:
    cs = stacks[fr-1][-quantity:]
    del stacks[fr-1][-quantity:]
    stacks[to-1].extend(cs)
  for s in stacks:
    if len(s) == 0:
      s.append(' ')
  return ''.join([s[-1] for s in stacks])