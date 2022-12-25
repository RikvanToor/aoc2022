import utils

def parse(input):
  return input.strip().split('\n')

def to_snafu(n):
  i = 0
  while True:
    highest_option = sum((5 ** x) * 2 for x in range(i+1))
    if highest_option >= n:
      break
    else:
      i += 1
  s = 0
  res = ''
  for j in range(i, -1, -1):
    options = [abs(n - (s + (5 ** j) * k)) for k in range(-2,3)]
    k = options.index(min(options))
    s += (5 ** j) * (k - 2)
    res += '=-012'[k]
  return res

def from_snafu(n):
  num = 0
  for i in range(len(n)):
    power = 5 ** i
    c = n[len(n)-1-i]
    match c:
      case '=':
        num -= power * 2
      case '-':
        num -= power
      case '1':
        num += power
      case '2':
        num += power * 2
  return num


def part_1(input):
  res = sum(map(from_snafu, input))
  return to_snafu(res)

def part_2(input):
  return 0