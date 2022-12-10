import utils

def parse(input):
  instructions = [l.split(' ') for l in input.rstrip().split('\n')]
  cycles = []
  for c in instructions:
    match c:
      case ['noop']:
        cycles.append(0)
      case ['addx', y]:
        cycles.append(0)
        cycles.append(int(y))
  return cycles

def part_1(input):
  result = 0
  for i in range(19, len(input)+1, 40):
    result += (1 + sum(input[0:i])) * (i + 1)
  return result

def part_2(input):
  lines = ''
  for i in range(len(input)+1):
    cur_x = i % 40
    if cur_x == 0:
      lines += '\n'
    xval = 1 + sum(input[0:i])
    if abs(xval - cur_x) <= 1:
      lines += '█'
    else:
      lines += ' '
  return lines