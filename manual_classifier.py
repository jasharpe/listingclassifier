from data import get_data, print_results
from classifier import Classifier
import random
import sys
from frozendict import UnenforcedFrozenDict

# A dict that provides a hash method so it can be used as the key in a dict.
# It should not be modified after construction, but this is not enforced.
class FakeFrozenDict(dict):
  def __hash__(self):
    return hash(tuple(sorted(self.items())))

if __name__ == "__main__":
  process_at_a_time = int(sys.argv[1])
  
  # Load data from files.
  listings = get_data("listings.txt")
  random.shuffle(listings)
  products = get_data("products.txt")
  classifier = Classifier(products)
  classified_listings = get_data("classified_listings.txt")

  old_listings = map(lambda x: UnenforcedFrozenDict(x['listing']), classified_listings)
  added = 0
  for listing in listings:
    if not UnenforcedFrozenDict(listing) in old_listings:
      print str(listing)
      suggested_product = classifier.classify(listing)
      if suggested_product is not None:
        print "Suggested product: %s" % str(suggested_product)
        yn = ''
        while not yn.lower() in ['y', 'n']:
          yn = raw_input('Is the suggested product correct? (y/n) ')
        if yn == 'y':
          product_name = suggested_product["product_name"]
        else:
          product_name = raw_input('Enter product name: ')
      else:
        product_name = raw_input('Enter product name: ')
      
      if product_name == '':
        classified_listings.append({'listing' : listing, 'product_name' : None })
      else:
        classified_listings.append({'listing' : listing, 'product_name' : product_name })
      added += 1
    if added == process_at_a_time:
      break
  
  print_results("classified_listings.txt", classified_listings)