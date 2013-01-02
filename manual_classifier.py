from data import get_data, print_results
import random

PROCESS_AT_A_TIME = 5

# A dict that provides a hash method so it can be used as the key in a dict.
# It should not be modified after construction, but this is not enforced.
class FakeFrozenDict(dict):
  def __hash__(self):
    return hash(tuple(sorted(self.items())))

if __name__ == "__main__":
  # Load data from files.
  listings = get_data("listings.txt")
  random.shuffle(listings)
  products = get_data("products.txt")
  classified_listings = get_data("classified_listings.txt")

  old_listings = map(lambda x: FakeFrozenDict(x['listing']), classified_listings)
  added = 0
  for listing in listings:
    #print old_listings
    #print listing
    #print
    if not FakeFrozenDict(listing) in old_listings:
      #print "Not skipped"
      print str(listing)
      product_name = raw_input('Enter product name: ')
      if product_name == '':
        classified_listings.append({'listing' : listing, 'product_name' : None })
      else:
        classified_listings.append({'listing' : listing, 'product_name' : product_name })
      added += 1
    if added == PROCESS_AT_A_TIME:
      break
  
  print_results("classified_listings.txt", classified_listings)