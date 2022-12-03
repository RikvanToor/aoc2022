import utils

def parse(input):
  return [(ord(m1) - ord('A'), ord(m2) - ord('X'))
    for x in input.strip().split('\n')
    for m1 in x[0]
    for m2 in x[2]]

def get_round_score(m1, m2):
  return m2 + 1 + ((((m2 - m1) % 3) + 1) % 3) * 3

def part_1(input):
  return sum([get_round_score(m1, m2) for (m1, m2) in input])

def part_2(input):
  return sum([get_round_score(m1, (m1 + (goal - 1)) % 3) for (m1, goal) in input])