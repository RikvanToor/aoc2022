def parse(input):
  return input.strip()

shapes = [
  [(0,0), (1,0), (2,0), (3,0)],
  [(0,1), (1,1), (2,1), (1,0), (1,2)],
  [(0,0), (1,0), (2,0), (2,1), (2,2)],
  [(0,0), (0,1), (0,2), (0,3)],
  [(0,0), (0,1), (1,0), (1,1)]
]

def add(p1, p2):
  (x1,y1) = p1
  (x2,y2) = p2
  return (x1+x2,y1+y2)

def move_rock(rock, d):
  return [add(p, d) for p in rock]

def rock_in_bounds(rock):
  for x,_ in rock:
    if x < 0 or x > 6:
      return False
  return True

def rock_move_valid(moved_rock, rock_set):
  return rock_in_bounds(moved_rock) and all([p not in rock_set for p in moved_rock])

def run(n, input, initial_rocks):
  highest_levels = [0 for _ in range(7)]
  rock_index = 0
  move_index = 0
  rock_set = initial_rocks
  
  for _ in range(n):
    active_rock = move_rock(shapes[rock_index], (2, max(highest_levels) + 4))
    rock_index = (rock_index + 1) % len(shapes)
    while True:
      c = input[move_index]
      if c == '>':
        move = (1,0)
      else:
        move = (-1,0)
      move_index = (move_index + 1) % len(input)

      moved_rock = move_rock(active_rock, move)
      if rock_move_valid(moved_rock, rock_set):
        active_rock = moved_rock

      dropped_rock = move_rock(active_rock, (0,-1))
      if not rock_move_valid(dropped_rock, rock_set):
        for p in active_rock:
          rock_set.add(p)
          if p[1] > highest_levels[p[0]]:
            highest_levels[p[0]] = p[1]
          min_max = min(highest_levels)
          rock_set = set([p for p in rock_set if p[1] >= min_max])
        break
      else:
        active_rock = dropped_rock

  return max(highest_levels)

def part_1(input):
  return run(2022, input, set([(x,0) for x in range(7)]))

def get_top_levels(n, rock_set, highest_level):
  return tuple(sorted([(x,y - highest_level) for (x,y) in rock_set if y > highest_level - n]))
  

def run2(n, input, initial_rocks):
  highest_levels = [0 for _ in range(7)]
  rock_index = 0
  move_index = 0
  rock_set = initial_rocks
  memo = {}
  finding_cycle = True
  
  i = 0
  while i <= n:
    if finding_cycle:
      top_n_levels = get_top_levels(10, rock_set, max(highest_levels))
      cache_key = (rock_index, move_index, top_n_levels)
      if cache_key in memo:
        mi, ml = memo[cache_key]
        repeat_range = i - mi
        repeat_height = max(highest_levels) - ml
        finding_cycle = False
        skip_factor = (n - mi) // repeat_range
        i = skip_factor * repeat_range + mi

        rock_set = set([(x,y + ml + skip_factor * repeat_height) for (x,y) in top_n_levels])
        maxy = max(highest_levels)
        highest_levels = [y - maxy + ml + skip_factor * repeat_height for y in highest_levels]
      else:
        memo[cache_key] = (i, max(highest_levels))
    active_rock = move_rock(shapes[rock_index], (2, max(highest_levels) + 4))
    rock_index = (rock_index + 1) % len(shapes)
    while True:
      c = input[move_index]
      if c == '>':
        move = (1,0)
      else:
        move = (-1,0)
      move_index = (move_index + 1) % len(input)

      moved_rock = move_rock(active_rock, move)
      if rock_move_valid(moved_rock, rock_set):
        active_rock = moved_rock

      dropped_rock = move_rock(active_rock, (0,-1))
      if not rock_move_valid(dropped_rock, rock_set):
        for p in active_rock:
          rock_set.add(p)
          if p[1] > highest_levels[p[0]]:
            highest_levels[p[0]] = p[1]
          min_max = min(highest_levels)
          rock_set = set([p for p in rock_set if p[1] >= min_max])
        break
      else:
        active_rock = dropped_rock
    
    i += 1

  return max(highest_levels)

def part_2(input):
  return run2(1000000000000, input, set([(x,0) for x in range(7)])) - 1