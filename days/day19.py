import utils
import re
from dataclasses import dataclass
import multiprocessing
import math

def parse(input):
  p = re.compile('\d+')
  return [tuple(map(int, p.findall(l))) for l in input.strip().split('\n')]

def get_moves(bp, s, moves_remaining):
  if moves_remaining == 0:
    return []
  bp_id, ore_robot_cost, clay_robot_cost, obsi_robot_cost_ore, obsi_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsi = bp
  moves = []
  ns = (s[0][0]+s[1][0],s[0][1]+s[1][1],s[0][2]+s[1][2],s[0][3]+s[1][3])
  if s[0][0] >= geode_robot_cost_ore and s[0][2] >= geode_robot_cost_obsi:
    
    moves.append(((ns[0] - geode_robot_cost_ore,ns[1],ns[2] - geode_robot_cost_obsi,ns[3]),(s[1][0],s[1][1],s[1][2],s[1][3]+1)))
  else:
    if s[0][0] >= ore_robot_cost:
      moves.append(((ns[0]-ore_robot_cost,ns[1],ns[2],ns[3]),(s[1][0]+1,s[1][1],s[1][2],s[1][3])))
    if s[0][0] >= clay_robot_cost:
      moves.append(((ns[0]-clay_robot_cost,ns[1],ns[2],ns[3]),(s[1][0],s[1][1]+1,s[1][2],s[1][3])))
    if s[0][0] >= obsi_robot_cost_ore and s[0][1] >= obsi_robot_cost_clay:
      moves.append(((ns[0]-obsi_robot_cost_ore,ns[1]-obsi_robot_cost_clay,ns[2],ns[3]),(s[1][0],s[1][1],s[1][2]+1,s[1][3])))
    moves.append((ns,s[1]))

  return moves

def max_score(bp, state, memo, best_memo, moves_remaining):
  potential = state[0][3] + moves_remaining * state[1][3]
  if best_memo[moves_remaining] > potential:
    return 0
  else:
    best_memo[moves_remaining] = potential
  if state in memo:
    return memo[state]
  if moves_remaining == 0:
    return state[0][3]
  moves = get_moves(bp, state, moves_remaining)
  res = max([max_score(bp, m, memo, best_memo, moves_remaining - 1) for m in moves])
  memo[state] = res
  return res

def max_score_pickle(input):
  bp, state, memo, best_memo, max_moves = input
  return max_score(bp, state, memo, best_memo, max_moves)

def part_1(input):
  with multiprocessing.Pool(12) as p:
    inputs = [(bp, ((0,0,0,0), (1,0,0,0)), {}, {x:0 for x in range(25)}, 24) for bp in input]
    res = p.map(max_score_pickle, inputs)
    return sum(map(math.prod, zip(range(1,len(input)+1), res)))

def part_2(input):
  with multiprocessing.Pool(12) as p:
    inputs = [(bp, ((0,0,0,0), (1,0,0,0)), {}, {x:0 for x in range(33)}, 32) for bp in input[0:3]]
    res = p.map(max_score_pickle, inputs)
    return math.prod(res)