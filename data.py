import json

def get_data(file_name):
  with open(file_name) as f:
    stripped_lines = map(lambda x: x.strip(), f.readlines())
    return map(json.loads, stripped_lines)
