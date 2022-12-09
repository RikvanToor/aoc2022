import utils

def parse(input):
  return [(l.split(' ')[0], int(l.split(' ')[1]))
          for l in input.rstrip().split('\n')]

def move(rope, dir, dist, visited):
  for _ in range(dist):
    rope[0][0] += dir[0]
    rope[0][1] += dir[1]
    for j in range(1, len(rope)):
      diffx = rope[j-1][0] - rope[j][0]
      diffy = rope[j-1][1] - rope[j][1]
      if diffx == 0 and abs(diffy) > 1:
        rope[j][1] += diffy // abs(diffy)
      elif abs(diffx) > 1 and diffy == 0:
        rope[j][0] += diffx // abs(diffx)
      elif (abs(diffx) > 1 or abs(diffy) > 1) and abs(diffx) >= 1 and abs(diffy) >= 1:
        rope[j][0] += diffx // abs(diffx)
        rope[j][1] += diffy // abs(diffy)
      if j == len(rope) - 1:
        visited.add((rope[j][0], rope[j][1]))

def solve(input, knot_count):
  rope = [[0, 0] for _ in range(knot_count)]
  visited = set()
  for (dir, dist) in input:
    match dir:
      case 'R': move(rope, (1, 0), dist, visited)
      case 'L': move(rope, (-1, 0), dist, visited)
      case 'U': move(rope, (0, 1), dist, visited)
      case 'D': move(rope, (0, -1), dist, visited)
  return len(visited)

def part_1(input):
  return solve(input, 2)

def part_2(input):
  return solve(input, 10)