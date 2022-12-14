import utils
import functools

def parse(input):
  pairs = input.rstrip().split('\n\n')
  return [(eval(p.split('\n')[0]), eval(p.split('\n')[1])) for p in pairs]

def compare(p1, p2):
  if type(p1) == int and type(p2) == list:
    return compare([p1], p2)
  if type(p1) == list and type(p2) == int:
    return compare(p1, [p2])
  if type(p1) == int:
    # both are ints
    return p1 <= p2, p1 == p2
  if type(p1) == list:
    # both are lists
    for i in range(len(p1)):
      if i >= len(p2):
        return False, False
      x = p1[i]
      y = p2[i]
      ok, equal = compare(x, y)
      if not ok:
        return False, False
      if not equal:
        return True, False
    return True, len(p1) == len(p2)

def cmp_sign(p1, p2):
  ok, equal = compare(p1, p2)
  match ok, equal:
    case _, True: return 0
    case True, False: return -1
    case False, False: return 1

def part_1(input):
  ok_list = []
  for j in range(len(input)):
    (p1, p2) = input[j]
    ok, _ = compare(p1, p2)
    if ok:
      ok_list.append(j+1)
  return sum(ok_list)

def part_2(input):
  ps = [p for pair in input for p in pair]
  ps.append([[6]])
  ps.append([[2]])
  s = sorted(ps, key=functools.cmp_to_key(cmp_sign))
  i1 = s.index([[2]]) + 1
  i2 = s.index([[6]]) + 1
  return i1 * i2