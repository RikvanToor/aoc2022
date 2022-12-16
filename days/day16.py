import utils
import re
import astar
from itertools import permutations, combinations

def parse_line(l):
  name = l[6:8]
  p = re.compile('\d+')
  rate = p.findall(l)[0]
  sc_index = l.find(';')
  leads_to_s = l[sc_index + 24:]
  leads_to = leads_to_s.strip().split(', ')
  return name, int(rate), leads_to

valves = {}

def parse(input):
  for l in input.rstrip().split('\n'):
    name, rate, leads_to = parse_line(l)
    valves[name] = (rate, leads_to)
  return valves

def calc_distance(v_from, v_to, memo):
  if v_to in valves[v_from][1]:
    memo[(v_from, v_to)] = 1
    memo[(v_to, v_from)] = 1
    return 1
  if (v_from, v_to) in memo:
    return memo[(v_from, v_to)]
  path = astar.find_path(
    v_from,
    v_to,
    lambda v: valves[v][1],
    False,
    lambda a, b: 1
  )
  res = len(list(path)) - 1
  memo[(v_from, v_to)] = res
  memo[(v_to, v_from)] = res
  return res

def solve_1(loc, unvisited, dist_memo, turns_remaining):
  max_score = 0
  best_order = []
  for u in unvisited:
    d = dist_memo[(loc,u)]
    new_tr = turns_remaining - d - 1
    if new_tr <= 0:
      continue
    local_score = new_tr * valves[u][0]
    sub_score, sub_path = solve_1(u, [u2 for u2 in unvisited if u != u2], dist_memo, new_tr)
    total_score = local_score + sub_score
    if total_score > max_score:
      max_score = total_score
      best_order = [u] + sub_path
  return max_score, best_order

def part_1(input):
  non_zeroes = [k for k in valves if valves[k][0] > 0]
  dist_memo = {}
  for x,y in combinations(non_zeroes + ['AA'], 2):
    calc_distance(x, y, dist_memo)
  best_score, _ = solve_1('AA', non_zeroes, dist_memo, 30)
  return best_score

def solve_2(my_loc, elephant_loc, my_timeout, elephant_timeout, unvisited, dist_memo, turns_remaining):
  time_skip = min(elephant_timeout, my_timeout)
  if time_skip > 0:
    return solve_2(my_loc, elephant_loc, my_timeout - time_skip, elephant_timeout - time_skip, unvisited, dist_memo, turns_remaining - time_skip)

  max_score = 0
  for u in unvisited:
    if my_timeout == 0:
      d = dist_memo[(my_loc, u)]
      new_tr = turns_remaining - d - 1
      if new_tr > 0:
        local_score = new_tr * valves[u][0]
        new_unvisited = [u2 for u2 in unvisited if u != u2]
        sub_score = solve_2(u, elephant_loc, d + 1, elephant_timeout, new_unvisited, dist_memo, turns_remaining)
        total_score = local_score + sub_score
        if total_score > max_score:
          max_score = total_score
    if elephant_timeout == 0:
      d = dist_memo[(elephant_loc, u)]
      new_tr = turns_remaining - d - 1
      if new_tr > 0:
        local_score = new_tr * valves[u][0]
        new_unvisited = [u2 for u2 in unvisited if u != u2]
        sub_score = solve_2(my_loc, u, my_timeout, d + 1, new_unvisited, dist_memo, turns_remaining)
        total_score = local_score + sub_score
        if total_score > max_score:
          max_score = total_score
  return max_score

def part_2(input):
  non_zeroes = [k for k in valves if valves[k][0] > 0]
  dist_memo = {}
  for x,y in combinations(non_zeroes + ['AA'], 2):
    calc_distance(x, y, dist_memo)
  best_score = solve_2('AA', 'AA', 0, 0, non_zeroes, dist_memo, 26)
  return best_score