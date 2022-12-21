import utils
from dataclasses import dataclass


class Node:
  def __init__(self, val):
    self.val = val
    self.or_prev: Node = None
    self.or_next: Node = None
    self.cur_prev: Node = None
    self.cur_next: Node = None

  def get_n(self, n):
    if n == 0:
      return self
    if n > 0:
      return self.cur_next.get_n(n - 1)
    return self.cur.prev.get_n(n + 1)
  
  def find(self, val):
    if self.val == val:
      return self
    return self.cur_next.find(val)

def get_n(node, n):
  cur = node
  while n != 0:
    if n > 0:
      cur = cur.cur_next
      n -= 1
    else:
      cur = cur.cur_prev
      n += 1
  return cur

def find(node, val):
  if node.val == val:
    return node
  cur = node.cur_next
  while cur != node:
    if cur.val == val:
      return cur
    cur = cur.cur_next

def parse(input):
  return list(map(int, input.strip().split('\n')))

def setup_list(input):
  first = Node(input[0])
  last = first
  for i in range(1, len(input)):
    n = Node(input[i])
    n.or_prev = last
    n.cur_prev = last
    last.or_next = n
    last.cur_next = n
    last = n
  first.or_prev = last
  first.cur_prev = last
  last.or_next = first
  last.cur_next = first
  return first

def mix(first, l):
  i = 0
  cur = first
  while cur != first or i == 0:
    steps = cur.val % (l - 1)
    neg_steps = steps - l
    if abs(neg_steps) < steps:
      steps = neg_steps
    if steps != 0:
      new_place = get_n(cur, steps)
      new_next = new_place.cur_next
      cur.cur_next.cur_prev = cur.cur_prev
      cur.cur_prev.cur_next = cur.cur_next
      cur.cur_next = new_next
      new_next.cur_prev = cur
      new_place.cur_next = cur
      cur.cur_prev = new_place
    cur = cur.or_next
    i += 1

def to_list(first):
  res = [first.val]
  cur = first.cur_next
  while cur != first:
    res.append(cur.val)
    cur = cur.cur_next
  return res

def run(input, n):
  first = setup_list(input)
  l = len(input)
  for _ in range(n):
    mix(first, l)
  zero = find(first, 0)
  n1000 = get_n(zero, 1000 % l).val
  n2000 = get_n(zero, 2000 % l).val
  n3000 = get_n(zero, 3000 % l).val
  return n1000 + n2000 + n3000

def part_1(input):
  return run(input, 1)

def part_2(input):
  input2 = [x * 811589153 for x in input]
  return run(input2, 10)