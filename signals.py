# Utility functions.

# Splits a string into a series of tokens. Currently just converts to lower case and splits on
# spaces.
def tokenize(string):
  return string.lower().replace("-", "").split(" ")

# Returns an index at which the subsequence ys appears consecutively in order in xs, or -1 if
# no such index exists, and the length of the matched subsequence.
def contains_subsequence(xs, ys):
  if ys == []:
    return (0, 0)
  for i in xrange(0, len(xs)):
    if xs[i:i+len(ys)] == ys:
      return (i, len(ys))
  return (-1, 0)
  
def merge_tokens(xs, merge_index):
  return xs[0:merge_index] + [xs[merge_index] + xs[merge_index + 1]] + xs[merge_index + 2:]

# For reference:
# Listing has "title", "manufacturer", "currency", and "price" fields.
# Product has "product_name", "manufacturer", "model", "family", "announced-date" fields.

# Strong positive signal if the model name appears in the title.
def model_name_signal(product, listing):
  listing_tokens = tokenize(listing["title"])
  product_tokens = tokenize(product["model"])
  match_length = contains_subsequence(listing_tokens, product_tokens)[1]
  if match_length:
    return match_length
  for merge_index in xrange(0, len(product_tokens) - 1):
    product_tokens_merged = merge_tokens(product_tokens, merge_index)
    match_length = contains_subsequence(listing_tokens, product_tokens_merged)[1]
    if match_length:
      return match_length
  return 0

# Strong negative signal if the product manufacturer isn't contained in the
# listing's manufacturer.
def manufacturer_name_signal(product, listing):
  listing_tokens = tokenize(listing["manufacturer"])
  product_tokens = tokenize(product["manufacturer"])
  return contains_subsequence(listing_tokens, product_tokens)[1]
  
def family_signal(product, listing):
  listing_tokens = tokenize(listing["title"])
  if not "family" in product:
    return True
  product_tokens = tokenize(product["family"])
  return contains_subsequence(listing_tokens, product_tokens)[1]