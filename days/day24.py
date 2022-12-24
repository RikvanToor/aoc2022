import utils
import astar

def parse(input):
  grid = [list(l) for l in input.strip().split('\n')]
  blizzards = []
  for y in range(1,len(grid)-1):
    for x in range(1,len(grid[y]) - 1):
      pos = (x-1,y-1)
      match grid[y][x]:
        case '.': continue
        case '>': blizzards.append((pos, (1, 0)))
        case '<': blizzards.append((pos, (-1, 0)))
        case 'v': blizzards.append((pos, (0, 1)))
        case '^': blizzards.append((pos, (0, -1)))
  dimensions = (len(grid[0])-2, len(grid)-2)

  return (blizzards, dimensions)

def add(p1, p2):
  x1,y1 = p1
  x2,y2 = p2
  return (x1+x2, y1+y2)

def get_blizzards_state(n, blizzards, dimensions, memo):
  if n in memo:
    return memo[n]
  width,height = dimensions
  new_blizzards = {((pos[0] + n * dir[0]) % width, (pos[1] + n * dir[1]) % height) for pos,dir in blizzards}
  memo[n] = new_blizzards
  return new_blizzards

def get_neighbours(state, blizzards, dimensions, blizzards_memo):
  pos,turn = state
  next_blizzards = get_blizzards_state(turn+1, blizzards, dimensions, blizzards_memo)
  if pos == (0,-1):
    new_poses = [(0,-1)] + [p for p in [(0,0)] if p not in next_blizzards]
  elif pos == (dimensions[0]-1,dimensions[1]):
    new_poses = [(dimensions[0]-1, dimensions[1])] + [p for p in [(dimensions[0]-1,dimensions[1]-1)] if p not in next_blizzards]
  else:
    new_poses = [p for p in [add(pos,p) for p in [(-1,0),(1,0),(0,-1),(0,1),(0,0)]] if p not in next_blizzards and 0 <= p[0] < dimensions[0] and 0 <= p[1] < dimensions[1] ]
  if pos == (dimensions[0]-1,dimensions[1]-1):
    new_poses.append((pos[0],pos[1]+1))
  if pos == (0,0):
    new_poses.append((0,-1))
  return [(p,turn+1) for p in new_poses]


def find_path(state, goal, blizzards, dimensions, memo):
  return astar.find_path(
    state,
    (goal, 1),
    lambda s: get_neighbours(s, blizzards, dimensions,memo),
    False,
    lambda a,b: abs(a[0][0]-b[0][0]) + abs(a[0][1]-b[0][1]),
    lambda a,b: 1,
    lambda a,b: a[0] == goal
  )

def part_1(input):
  blizzards, dimensions = input
  memo = {}
  state = ((0,-1), 0)
  goal = (dimensions[0]-1,dimensions[1])
  path = find_path(state, goal, blizzards, dimensions, memo)
  lp = list(path)
  return len(lp) - 1

def part_2(input):
  blizzards, dimensions = input
  memo = {}
  state1 = ((0,-1), 0)
  goal1 = (dimensions[0]-1,dimensions[1])
  path1 = find_path(state1, goal1, blizzards, dimensions, memo)
  lp1 = list(path1)
  state2 = lp1[-1]
  path2 = find_path(state2, (0,-1), blizzards, dimensions, memo)
  lp2 = list(path2)
  state3 = lp2[-1]
  path3 = find_path(state3, goal1, blizzards, dimensions, memo)
  lp3 = list(path3)
  return len(lp1) + len(lp2) + len(lp3) - 3