import utils

def parse(input):
  return input.strip()

def solve(input, size):
  for i in range(len(input) - size + 1):
    slice = input[i:i+size]
    if len(set(slice)) == size:
      return i + size
  return -1

def part_1(input):
  return solve(input, 4)

def part_2(input):
  return solve(input, 14)