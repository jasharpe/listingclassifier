# A dict that provides a hash method so it can be used as the key in a dict.
# It should not be modified after construction, but this is not enforced.
class UnenforcedFrozenDict(dict):
  def __hash__(self):
    return hash(tuple(sorted(self.items())))