import utils

def parse(input):
  cmds = [(c.split('\n')[0], c.rstrip().split('\n')[1:]) for c in input.rstrip().split('$ ')[1:]]
  return build_tree(cmds)

def build_tree(input):
  tree = {}
  cp = []
  for (c, res) in input:
    cs = c.split(' ')
    cmd = cs[0]
    args = cs[1:]
    match cmd:
      case 'cd':
        match args[0]:
          case '/':
            cp = ['/']
          case '..':
            cp.pop()
          case x:
            cp.append(x)
        add_dir(tree, cp)
      case 'ls':
        for r in res:
          [dir_or_size, path] = r.split(' ')
          match dir_or_size:
            case 'dir':
              add_dir(tree, cp + [path])
            case size:
              add_file_size(tree, cp, path, int(size))
  return tree

def part_1(input):
  all_dirs = get_all_dirs(input)
  return sum([path_to_size(input,d) for d in all_dirs if path_to_size(input,d) <= 100000])

def part_2(input):
  total_size = sum_tree(input)
  disk_size = 70000000
  minimum_space_needed = 30000000
  to_delete = total_size - (disk_size - minimum_space_needed)
  all_dirs = get_all_dirs(input)
  all_dirs_sizes = [path_to_size(input,d) for d in all_dirs]
  large_enough = [s for s in all_dirs_sizes if s >= to_delete]
  return min(large_enough)

def path_to_node(tree, path):
  cn = tree
  for p in path:
    cn = cn[p]
  return cn

def add_dir(tree, path):
  cn = path_to_node(tree, path[0:-1])
  if path[-1] not in cn:
    cn[path[-1]] = {}

def add_file_size(tree, dir_path, file_name, size):
  cn = path_to_node(tree, dir_path)
  cn[file_name] = size

def get_all_dirs(tree, prefix = [], stack = []):
  for p in tree:
    if type(tree[p]) == dict:
      stack.append(prefix + [p])
      get_all_dirs(tree[p], prefix + [p], stack)
  return stack

def path_to_size(tree, path):
  n = path_to_node(tree, path)
  return sum_tree(n)

def sum_tree(tree):
  res = 0
  for p in tree:
    if type(tree[p]) == int:
      res += tree[p]
    elif type(tree[p]) == dict:
      res += sum_tree(tree[p])
  return res