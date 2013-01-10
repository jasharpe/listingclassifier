import re

# Utility functions.

# Splits a string into a series of tokens. Currently just converts to lower case and splits on
# spaces.
first_letter_smushing_pattern = re.compile(r"\b([a-z]) ")
def tokenize(string):
  # Commented out code removes spaces between single letters and the next word, which seems to
  # be more helpful than harmful, but is also really slow, and kind of speculative given my
  # small training set.
  stripped_string = (#re.sub(first_letter_smushing_pattern, r"\1",
      string.lower()
          .replace("-", "")
          .replace(";", "")
          .replace("+", " ")
          # Some camera specific abbreviations that are erratically used. This will be useless
          # for non-camera verticals. 
          .replace("dmc", "")
          .replace("is", "")
          .replace("dsc", "")
          .replace("pen", "")
          .replace("dslr", ""))
  
  return filter(None, stripped_string.split(" "))

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

# Checks if the model name appears in the title.
def model_name_signal(product, listing):
  # Only consider the first 6 tokens of the listing, since interesting information is likely
  # to occur early in the listing, whereas model names late in listing are probably not the
  # main subject.
  listing_tokens = tokenize(listing["title"])[:6]
  product_tokens = tokenize(product["model"])
  match_length = contains_subsequence(listing_tokens, product_tokens)[1]
  if match_length:
    return match_length
  # Try removing one space at a time in the product's model string, and attempt to match.
  # This matches things where spaces don't quite match.
  for merge_index in xrange(0, len(product_tokens) - 1):
    product_tokens_merged = merge_tokens(product_tokens, merge_index)
    match_length = contains_subsequence(listing_tokens, product_tokens_merged)[1]
    if match_length:
      return match_length
  # This improves matching, but is quite slow. Doubles already slow time.
  #for merge_index in xrange(0, min(3, len(listing_tokens) - 1)):
  #  listing_tokens_merged = merge_tokens(listing_tokens, merge_index)
  #  match_length = contains_subsequence(listing_tokens_merged, product_tokens)[1]
  #  if match_length:
  #    return match_length
  return 0

# Checks if the manufacturer appears in the manufacturer or title sections of the listing.
def manufacturer_name_signal(product, listing):
  listing_tokens = tokenize(listing["manufacturer"])
  product_tokens = tokenize(product["manufacturer"])
  result = contains_subsequence(listing_tokens, product_tokens)[1] 
  if result == 0:
    # Check in the listing's title instead.
    listing_tokens = tokenize(listing["title"])
    return contains_subsequence(listing_tokens, product_tokens)[1]
  else:
    return result

# Checks if the product family appears in the listing.
def family_signal(product, listing):
  listing_tokens = tokenize(listing["title"])
  if not "family" in product:
    return True
  product_tokens = tokenize(product["family"])
  return contains_subsequence(listing_tokens, product_tokens)[1]