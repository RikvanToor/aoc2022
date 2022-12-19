import utils
import re
from dataclasses import dataclass
import multiprocessing
import math

def parse(input):
  p = re.compile('\d+')
  return [tuple(map(int, p.findall(l))) for l in input.strip().split('\n')]

@dataclass(eq=True, frozen=True)
class State:
  ore_robots: int = 1
  clay_robots: int = 0
  obsi_robots: int = 0
  geode_robots: int = 0
  ore: int = 0
  clay: int = 0
  obsi: int = 0
  geode: int = 0
  move_count: int = 0

def get_new_state(bp, move, s):
  bp_id, ore_robot_cost, clay_robot_cost, obsi_robot_cost_ore, obsi_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsi = bp
  orbs, clbs, obbs, gebs = move
  return State(
    ore = s.ore + s.ore_robots - orbs * ore_robot_cost - clbs * clay_robot_cost - obbs * obsi_robot_cost_ore - gebs * geode_robot_cost_ore,
    clay = s.clay + s.clay_robots - obbs * obsi_robot_cost_clay,
    obsi = s.obsi + s.obsi_robots - gebs * geode_robot_cost_obsi,
    geode = s.geode + s.geode_robots,
    ore_robots = s.ore_robots + orbs,
    clay_robots = s.clay_robots + clbs,
    obsi_robots = s.obsi_robots + obbs,
    geode_robots = s.geode_robots + gebs
  )

def get_moves(bp, state, moves_remaining):
  if moves_remaining == 0:
    return []
  bp_id, ore_robot_cost, clay_robot_cost, obsi_robot_cost_ore, obsi_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsi = bp
  moves = []
  if state.ore >= geode_robot_cost_ore and state.obsi >= geode_robot_cost_obsi:
    moves.append((0,0,0,1))
  else:
    if state.ore >= ore_robot_cost:
      moves.append((1,0,0,0))
    if state.ore >= clay_robot_cost:
      moves.append((0,1,0,0))
    if state.ore >= obsi_robot_cost_ore and state.clay >= obsi_robot_cost_clay:
      moves.append((0,0,1,0))
    moves.append((0,0,0,0))

  return moves

def max_score(bp, state, memo, best_memo, moves_remaining):
  potential = state.geode + moves_remaining * state.geode_robots
  if best_memo[moves_remaining] > potential:
    return 0
  else:
    best_memo[moves_remaining] = potential
  if state in memo:
    return memo[state]
  if moves_remaining == 0:
    return state.geode
  moves = get_moves(bp, state, moves_remaining)
  res = max([max_score(bp, get_new_state(bp, m, state), memo, best_memo, moves_remaining - 1) for m in moves])
  memo[state] = res
  return res

def max_score_pickle(input):
  bp, state, memo, best_memo, max_moves = input
  return max_score(bp, state, memo, best_memo, max_moves)

def part_1(input):
  with multiprocessing.Pool(12) as p:
    inputs = [(bp, State(), {}, {x:0 for x in range(25)}, 24) for bp in input]
    res = p.map(max_score_pickle, inputs)
    return sum(map(math.prod, zip(range(1,len(input)+1), res)))

def part_2(input):
  with multiprocessing.Pool(12) as p:
    inputs = [(bp, State(), {}, {x:0 for x in range(33)}, 32) for bp in input[0:3]]
    res = p.map(max_score_pickle, inputs)
    return math.prod(res)