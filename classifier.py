from collections import defaultdict

# Strong positive signal if the model name appears in the title.
def model_name_signal(product, listing):
  if " " in product['model']:
    if product['model'].lower() in listing["title"].lower():
      return 100
  else:
    if product['model'].lower() in listing["title"].lower().split(" "):
      return 100
  return 0

def manufacturer_name_signal(product, listing):
  if product["manufacturer"].lower() != listing["manufacturer"].lower():
    return -100
  return 0

AMBIGUITY_THRESHOLD = 5

class Classifier(object):
  def __init__(self, products):
    self.products = products

  # Returns the product name that most closely matches listing. If two products closely match, or there are no close matches, returns None.
  def classify(self, listing):
    # Listing has "title", "manufacturer", "currency", and "price" fields.
    # Product has "product_name", "manufacturer", "model", "family", "announced-date" fields.
    signals = [
      model_name_signal,
      manufacturer_name_signal,
    ]

    candidate_products = defaultdict(int)
    for product in self.products:
      positive_signals = sum(map(lambda signal: signal(product, listing), signals))
      if positive_signals > 0:
        candidate_products[product["product_name"]] = positive_signals
    
    product_ratings = list(reversed(sorted(candidate_products.items(), key=lambda x: x[1])))

    if len(product_ratings) == 0:
      print "Failed on %s, because there were no candidates" % (str(listing))
      return None
    elif len(product_ratings) == 1:
      return product_ratings[0][0]
    elif abs(product_ratings[0][1] - product_ratings[1][1]) < AMBIGUITY_THRESHOLD:
      print "Failed on %s, because there were at least two plausible candidates:\n%s\n%s" % (str(listing), str(product_ratings[0][0]), str(product_ratings[1][0]))
      print product_ratings
      return None
    else:
      return product_ratings[0][0]
