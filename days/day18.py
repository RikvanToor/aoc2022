import utils
import astar

def parse(input):
  return [tuple(map(lambda x: int(x), l.split(','))) for l in input.rstrip().split('\n')]

def add(c1, c2):
  x1,y1,z1 = c1
  x2,y2,z2 = c2
  return (x1+x2, y1+y2, z1+z2)

adjacents = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

def part_1(input):
  return sum(1 for c in input for d in adjacents if add(c,d) not in input)

def get_all_trapped_neighbours(n, input, seen_set=set()):
  seen_set.add(n)
  for n2 in [n2 for n2 in [add(n,d) for d in adjacents] if n2 not in seen_set and n2 not in input]:
    get_all_trapped_neighbours(n2, input, seen_set)
  return seen_set

def part_2(input):
  neighbours = set()
  for c in input:
    for d in adjacents:
      n = add(c, d)
      if n not in input:
        neighbours.add(n)

  xs = [x for x,y,z in input]
  ys = [y for x,y,z in input]
  zs = [z for x,y,z in input]
  min_x = min(xs)
  min_y = min(ys)
  min_z = min(zs)
  goal_point = (min_x-1, min_y-1, min_z-1)

  trapped_neighbours = set()
  free_points = {goal_point}
  for n in neighbours:
    if n in trapped_neighbours or n in free_points:
      continue
    escape_path = astar.find_path(
      n,
      goal_point,
      lambda x: [p for p in [add(x, d) for d in adjacents] if p not in input],
      False,
      lambda a,b: abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]+b[2]),
      lambda a,b: 1,
      lambda a,b: a in free_points
    )
    if escape_path == None:
      for n2 in get_all_trapped_neighbours(n, input):
        trapped_neighbours.add(n2)
    else:
      for p in list(escape_path):
        free_points.add(p)

  return sum(1 for p in [add(c, d) for c in input for d in adjacents]
               if p not in input and p not in trapped_neighbours)