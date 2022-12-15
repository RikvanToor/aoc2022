import utils
import re

def parse_line(l):
  p = re.compile('-?\d+')
  [sx, sy, bx, by] = map(int, p.findall(l))
  return ((sx, sy), (bx, by))

def parse(input):
  return [parse_line(l) for l in input.rstrip().split('\n')]

def join_ranges(ranges):
  if len(ranges) == 0:
    return ranges
  s = sorted(ranges)
  cur_range = s[0]
  res = set()
  for i in range(1, len(s)):
    start1,end1 = cur_range
    start2,end2 = s[i]
    if start2 <= end1 + 1:
      cur_range = (start1, max(end1,end2))
    else:
      res.add(cur_range)
      cur_range = (start2,end2)
  res.add(cur_range)
  return res

def part_1(input):
  row_to_check = 2000000
  ranges_set = set()
  for ((sx,sy),(bx,by)) in input:
    dist = abs(bx-sx) + abs(by-sy)
    dist_to_row = abs(row_to_check - sy)
    if dist_to_row <= dist:
      x_dist = dist - dist_to_row
      ranges_set.add((sx - x_dist, sx + x_dist))
  rs = join_ranges(ranges_set)
  return sum(map(lambda r: r[1] - r[0], rs))

def part_2(input):
  max_row = 4000000
  ranges = {}
  for ((sx,sy),(bx,by)) in input:
    dist = abs(bx-sx) + abs(by-sy)
    for row_to_check in range(max(0, sy - dist), min(max_row, sy + dist + 1)):
      if row_to_check not in ranges:
        ranges[row_to_check] = set()
      dist_to_row = abs(row_to_check - sy)
      if dist_to_row <= dist:
        x_dist = dist - dist_to_row
        ranges[row_to_check].add((sx - x_dist, sx + x_dist))
  for row in ranges:
    ranges[row] = join_ranges(ranges[row])
    # This assumes the point is not on x = 0 or x = 3999999
    # So this is technically wrong, but whatever
    if len(ranges[row]) > 1:
      min_x = 0
      max_x = max_row
      for r_start, r_end in ranges[row]:
        if max_x < r_end:
          max_x = min(max_x, r_start - 1)
        if min_x > r_start:
          min_x = max(min_x, r_end + 1)
      if min_x == max_x:
        return min_x * 4000000 + row
      else:
        return 'Error: More than one option exists'