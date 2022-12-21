import utils
import re

def parse_line(l):
  (name, func) = l.split(': ')
  f = 'lambda d: ' + re.sub('([a-z]+)', r"run('\1', d)", func)
  if f.isdigit():
    data = int(func)
  else:
    data = func.split(' ')
  return (name, (eval(f), data))

def parse(input):
  dict = {}
  for l in input.rstrip().split('\n'):
    (name, f) = parse_line(l)
    dict[name] = f
  return dict

def run(name, d):
  (f,_) = d[name]
  return int(f(d))

def part_1(input):
  return run('root', input)

def find_humn(name, d):
  if name == 'humn':
    return True
  (_, data) = d[name]
  match data:
    case [n1, op, n2]: return find_humn(n1, d) or find_humn(n2, d)
    case _: return False

def run_2(name, d, goal):
  if name == 'humn':
    return goal
  # This function should not be run with keys that return literal ints
  (_, (n1, op, n2)) = d[name]
  left_known = find_humn(n2, d)
  if left_known:
    known_side = run(n1, d)
    unknown_side = n2
  else:
    known_side = run(n2, d)
    unknown_side = n1

  if op == '+':
    return run_2(unknown_side, d, goal - known_side)
  if op == '-':
    if left_known:
      return run_2(unknown_side, d, -(goal - known_side))
    else:
      return run_2(unknown_side, d, goal + known_side)
  if op == '*':
    return run_2(unknown_side, d, goal / known_side)
  if op == '/':
    if left_known:
      return run_2(unknown_side, d, known_side / goal)
    else:
      return run_2(unknown_side, d, goal * known_side)
  return 'unknown operator: ' + op
  

def part_2(input):
  (_, [n1, op, n2]) = input['root']
  if find_humn(n1, input):
    goal = run(n2, input)
    humn_side = n1
  else:
    goal = run(n1, input)
    humn_side = n2
  return int(run_2(humn_side, input, goal))