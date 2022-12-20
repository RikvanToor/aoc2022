import utils

def parse(input):
  return list(map(int, input.strip().split('\n')))

def mix(input, n = 1):
  li = len(input)
  or_to_new = {x:x for x in range(li)}
  new_to_or = {x:x for x in range(li)}
  for _ in range(n):
    for i in range(li):
      val = input[i]
      if or_to_new[i] + val <= 0 and val != 0:
        val = val % (li - 1)
      elif or_to_new[i] + val >= li - 1 and val != 0:
        val = val % (li - 1) - li + 1
      old_pos = or_to_new[i]
      new_pos = (or_to_new[i] + val)

      for j in range(old_pos, new_pos):
        new_to_or[j % li] = new_to_or[(j+1) % li]
        or_to_new[new_to_or[j % li]] = j % li
      for j in range(old_pos, new_pos, -1):
        new_to_or[j % li] = new_to_or[(j-1) % li]
        or_to_new[new_to_or[j % li]] = j % li
      new_to_or[new_pos % li] = i
      or_to_new[i] = new_pos % li
  return [input[new_to_or[x]] for x in range(li)]

def get_result(input):
  li = len(input)
  zero = input.index(0)
  return input[(zero + 1000) % li] + input[(zero + 2000) % li] + input[(zero + 3000) % li]

def part_1(input):
  return get_result(mix(input, 1))

def part_2(input):
  input2 = [x * 811589153 for x in input]
  return get_result(mix(input2, 10))