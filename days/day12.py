import utils
import astar

grid = []

def parse(input):
  cur_pos = (0, 0)
  goal = (0, 0)
  ls = input.rstrip().split('\n')
  for y in range(len(ls)):
    row = []
    for x in range(len(ls[y])):
      c = ls[y][x]
      if c == 'S':
        cur_pos = (x, y)
        row.append(0)
      elif c == 'E':
        goal = (x, y)
        row.append(25)
      else:
        row.append(ord(c) - ord('a'))
    grid.append(row)

  return (grid, cur_pos, goal)

def ok_move(val1, val2):
  return val2 <= val1 + 1

def get_neighbours(pos, invert=False):
  (x, y) = pos
  ds = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  ns = [(x + dx, y + dy)
        for dx, dy in ds
        if 0 <= x + dx < len(grid[0])
        if 0 <= y + dy < len(grid)
        if (grid[y+dy][x+dx] - grid[y][x] <= 1
            if not invert
            else grid[y+dy][x+dx] - grid[y][x] >= -1)
       ]
  return ns

def part_1(input):
  (_, start_pos, goal) = input
  res = astar.find_path(
    start_pos,
    goal,
    get_neighbours,
    heuristic_cost_estimate_fnct= lambda a, b: 1
  )
  path = list(res)
  return len(path) - 1

def part_2(input):
  (_, start_pos, goal) = input
  res = astar.find_path(
    goal,
    start_pos,
    lambda n: get_neighbours(n, True),
    heuristic_cost_estimate_fnct= lambda a, b: 1,
    is_goal_reached_fnct=lambda pos_a,pos_b: grid[pos_a[1]][pos_a[0]] == 0,
  )
  path = list(res)
  return len(path) - 1