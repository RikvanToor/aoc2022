import utils
import numpy as np

def parse_instructions(input):
  res = []
  i = 0
  while i < len(input):
    if input[i].isnumeric():
      num_start = i
      num_end = i
      for j in range(i+1, len(input)):
        if input[j].isnumeric():
          num_end = j
        else:
          break
      res.append(int(input[num_start:num_end+1]))
      i = num_end + 1
    else:
      res.append(input[i])
      i += 1
  return res

def parse(input):
  [m, i] = input.rstrip().split('\n\n')
  return (m.split('\n'), parse_instructions(i))

def add(p1, p2):
  x1,y1 = p1
  x2,y2 = p2
  return (x1+x2,y1+y2)

def substract(p1, p2):
  x1,y1 = p1
  x2,y2 = p2
  return (x1-x2,y1-y2)

def turn_cw(p):
  x,y = p
  return (-y, x)

def turn_ccw(p):
  x,y = p
  return (y, -x)

def get_h_bounds(m):
  res = []
  for l in m:
    min_x = len(l) - 1
    max_x = 0
    for x in range(len(l)):
      c = l[x]
      if c != ' ':
        min_x = min(min_x, x)
        max_x = max(max_x, x)
    res.append((min_x, max_x))
  return res

def get_v_bounds(m):
  res = []
  for x in range(max(map(len, m))):
    min_y = len(m) - 1
    max_y = 0
    for y in range(len(m)):
      if len(m[y]) > x and m[y][x] != ' ':
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    res.append((min_y, max_y))
  return res

def dir_to_value(dir):
  match dir:
    case (1,0):  return 0
    case (0,1):  return 1
    case (-1,0): return 2
    case (0,-1): return 3

def part_1(input):
  m, path = input
  h_bounds = get_h_bounds(m)
  v_bounds = get_v_bounds(m)
  dir = (1,0)
  pos = (h_bounds[0][0], 0)
  for p in path:
    match p:
      case 'R':
        dir = turn_cw(dir)
      case 'L':
        dir = turn_ccw(dir)
      case _:
        for _ in range(p):
          new_x,new_y = add(pos, dir)
          if dir[1] == 0:
            # Horizontal movement
            hb_min,hb_max = h_bounds[new_y]
            if new_x < hb_min or new_x > hb_max:
              new_x = ((new_x - hb_min) % (hb_max - hb_min + 1)) + hb_min
          else:
            vb_min,vb_max = v_bounds[new_x]
            if new_y < vb_min or new_y > vb_max:
              new_y = ((new_y - vb_min) % (vb_max - vb_min + 1)) + vb_min
          if m[new_y][new_x] == '#':
            break
          else:
            pos = (new_x, new_y)
  return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + dir_to_value(dir)

def create_cube(m):
  # My brain is melting.
  # Hardcoding. 😞
  max_len = max(map(len, m))
  cube_str = [[(l[i] if i < len(l) else ' ') for i in range(max_len)] for l in m]
  total_arr = np.array(cube_str)
  pos_arr = np.array([[(x,y) for x in range(1, max_len+1)] for y in range(1, len(m) + 1)])
  if len(m[0]) == 12:
    # Test cube
    top = total_arr[0:4,8:12]
    left = total_arr[4:8,4:8]
    front = total_arr[4:8,8:12]
    right = np.rot90(total_arr[8:12,12:16], 1, (0,1))
    back = total_arr[4:8,0:4]
    bottom = total_arr[8:12,8:12]

    pos_top = pos_arr[0:4,8:12]
    pos_left = pos_arr[4:8,4:8]
    pos_front = pos_arr[4:8,8:12]
    pos_right = np.rot90(pos_arr[8:12,12:16], 1, (0,1))
    pos_back = pos_arr[4:8,0:4]
    pos_bottom = pos_arr[8:12,8:12]
    return ((top, left, front, right, back, bottom), (pos_top, pos_left, pos_front, pos_right, pos_back, pos_bottom))
  else:
    # Real cube
    top = total_arr[0:50,50:100]
    left = np.rot90(total_arr[100:150,0:50], 1, (1, 0))
    front = total_arr[50:100,50:100]
    right = np.rot90(total_arr[0:50,100:150], 1, (1, 0))
    back = np.rot90(total_arr[150:200,0:50], 1, (1, 0))
    bottom = total_arr[100:150,50:100]

    pos_top = pos_arr[0:50,50:100]
    pos_left = np.rot90(pos_arr[100:150,0:50], 1, (1, 0))
    pos_front = pos_arr[50:100,50:100]
    pos_right = np.rot90(pos_arr[0:50,100:150], 1, (1, 0))
    pos_back = np.rot90(pos_arr[150:200,0:50], 1, (1, 0))
    pos_bottom = pos_arr[100:150,50:100]
    return ((top, left, front, right, back, bottom), (pos_top, pos_left, pos_front, pos_right, pos_back, pos_bottom))

def get_target(pos, dir, dimension):
  s, x, y = pos
  # s: 0 => top, 1 => left, 2 => front, 3 => right, 4 => back, 5 => bottom
  new_x, new_y = add((x, y), dir)
  if new_x == -1:
    match s:
      case 0: return ((1, y, 0), (0, 1))
      case 1: return ((4, dimension - 1, y), dir)
      case 2: return ((1, dimension - 1, y), dir)
      case 3: return ((2, dimension - 1, y), dir)
      case 4: return ((3, dimension - 1, y), dir)
      case 5: return ((1, dimension - 1 - y, dimension - 1), (0, -1))
  if new_x == dimension:
    match s:
      case 0: return ((3, dimension - 1 - y, 0), (0, 1))
      case 1: return ((2, 0, y), dir)
      case 2: return ((3, 0, y), dir)
      case 3: return ((4, 0, y), dir)
      case 4: return ((1, 0, y), dir)
      case 5: return ((3, y, dimension - 1), (0, -1))
  if new_y == -1:
    match s:
      case 0: return ((4, dimension - 1 - x, 0), (0, 1))
      case 1: return ((0, 0, x), (1, 0))
      case 2: return ((0, x, dimension - 1), dir)
      case 3: return ((0, dimension - 1, dimension - 1 - x), (-1, 0))
      case 4: return ((0, dimension - 1 - x, 0), (0, 1))
      case 5: return ((2, x, dimension - 1), dir)
  if new_y == dimension:
    match s:
      case 0: return ((2, x, 0), dir)
      case 1: return ((5, 0, dimension - 1 - x), (1, 0))
      case 2: return ((5, x, 0), dir)
      case 3: return ((5, dimension - 1, x), (-1, 0))
      case 4: return ((5, dimension - 1 - x, dimension - 1), (0, -1))
      case 5: return ((4, dimension - 1 - x, dimension - 1), (0, -1))
  return ((s, new_x, new_y), dir)


def part_2(input):
  m, path = input
  dimension = 4 if len(m[0]) == 12 else 50
  print(dimension)
  sides, poss = create_cube(m)
  pos = (0, 0, 0)
  dir = (1, 0)
  for p in path:
    match p:
      case 'R':
        dir = turn_cw(dir)
      case 'L':
        dir = turn_ccw(dir)
      case _:
        for _ in range(p):
          (new_pos, new_dir) = get_target(pos, dir, dimension)
          s, new_x, new_y = new_pos
          c = sides[s][new_y,new_x]
          if c == '#':
            break
          else:
            pos = new_pos
            dir = new_dir
  x,y =  poss[pos[0]][pos[2],pos[1]]
  temp = poss[pos[0]][1+dir[1],1+dir[0]]
  true_dir = substract(temp, poss[pos[0]][1,1])
  return 1000 * y + 4 * x + dir_to_value(true_dir)
