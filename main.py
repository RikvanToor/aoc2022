#!/usr/bin/python3

from datetime import date
import sys
from os.path import exists
import requests
import importlib
import time
import copy

YEAR = 2022

def get_day():
  if len(sys.argv) > 2 and sys.argv[2].isnumeric():
    day = int(sys.argv[2])
    if day < 1 or day > 25:
      raise Exception(f'Not a valid day: {day}')
    return day
  else:
    d = date.today()
    if d.year == YEAR and d.month == 12 and d.day <= 25:
      return d.day
    else:
      raise Exception(f'No valid day supplied')

def parse_args():
  if len(sys.argv) > 1:
    if sys.argv[1] == 'get-input':
      day = get_day()
      get_input(day)
    elif sys.argv[1] == 'run':
      day = get_day()
      run(day)
  else:
    print('Add a command: get-input | run')

def get_input(day):
  if exists('.cookie'):
    with open('.cookie') as c:
      cookie = c.read().strip()
    h = {'Cookie': f'session={cookie}'}
    r = requests.get(url = f'https://adventofcode.com/{YEAR}/day/{day}/input', headers = h)
    with open(f'inputs/day{day:02d}.txt', 'w') as f:
      f.write(r.text)
    print('Done')
  else:
    raise Exception('Add your AoC cookie to a file called .cookie')

def run(day):
  input_file = f'inputs/day{day:02d}.txt'
  if not exists(input_file):
    get_input(day)
  with open(input_file) as f:
    input = f.read()

    print(f'======== DAY {day} ========')
    mod = importlib.import_module(f'days.day{day:02d}')
    p = mod.parse(input)
    p2 = copy.deepcopy(p)
    start_time = time.time()
    print(f'Part 1: {mod.part_1(p)}')
    p1_time = time.time()
    print(f'Part 1 took {p1_time - start_time}s')
    print(f'Part 2: {mod.part_2(p2)}')
    p2_time = time.time()
    print(f'Part 2 took {p2_time - p1_time}s')
  
parse_args()