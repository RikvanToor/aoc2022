import utils
import numpy as np
from math import prod

def parse(input):
  return [list(map(int, l)) for l in input.rstrip().split('\n')]

def part_1(input):
  arr = np.array(input)
  counter = 0
  for y in range(1, len(input) - 1):
    for x in range(1, len(input[y]) - 1):
      val = arr[y,x]
      top = max(arr[0:y,x])
      bottom = max(arr[y+1:,x])
      left = max(arr[y,0:x])
      right = max(arr[y,x+1:])
      if min(top, bottom, left, right) < val:
        counter += 1
  (height, width) = np.shape(arr)
  return counter + 2 * height + 2 * (width - 2)

def calc_score(path, val):
  score = 0
  for p in path:
    score += 1
    if p >= val:
      return score
  return score

def part_2(input):
  arr = np.array(input)
  best_score = 0
  for y in range(1, len(input) - 1):
    for x in range(1, len(input[y]) - 1):
      val = arr[y,x]
      top = np.flip(arr[0:y,x])
      bottom = arr[y+1:,x]
      left = np.flip(arr[y,0:x])
      right = arr[y,x+1:]
      score = prod([calc_score(p, val) for p in [top, bottom, left, right]])
      if score > best_score:
        best_score = score
  return best_score