#!/usr/bin/python
from data import get_data, print_results
from classifier import Classifier
from collections import defaultdict
import argparse
import sys
from frozendict import UnenforcedFrozenDict

def main():
  # Parse command line arguments
  parser = argparse.ArgumentParser(description="""
Shopping listing classifier tool. Run in a directory containing listings.txt and products.txt. Produces results.txt.""")
  parser.add_argument('-v','--verbose', help='display extra information for debugging',
      action='store_true')
  parser.add_argument('-d','--diagnostic', help='use classified_listings.txt, which contains listings with correct products.',
      action='store_true')
  args = parser.parse_args()
  
  # Load data from files.
  products = get_data("products.txt")
  if args.diagnostic:
    classified_listings = get_data("classified_listings.txt")
    listings = map(lambda x: x["listing"], classified_listings)
    listing_to_product = {}
    for classified_listing in classified_listings:
      product_name = classified_listing["product_name"]
      listing = UnenforcedFrozenDict(classified_listing["listing"])
      listing_to_product[listing] = product_name
  else:
    listings = get_data("listings.txt")

  # Create a classifier for the provided products.
  classifier = Classifier(products)

  # Classify all listings.
  results = defaultdict(list)
  classified = 0
  correct = 0
  positive_error = 0
  negative_error = 0
  for listing in listings:
    product = classifier.classify(listing, verbose=args.verbose)
    if args.diagnostic:
      correct_product_name = listing_to_product[UnenforcedFrozenDict(listing)]
    if product is None:
      if args.diagnostic and correct_product_name is not None:
        print "NEGATIVE ERROR: None instead of %s\nListing: %s\n" % (correct_product_name, str(listing))
        negative_error += 1
      elif args.diagnostic:
        correct += 1
    else:
      classified += 1
      product_name = product["product_name"]
      results[product_name].append(listing)
      if args.diagnostic and product_name != correct_product_name:
        positive_error += 1
        print "POSITIVE ERROR: %s instead of %s\nListing: %s\n" % (product_name, correct_product_name, str(listing))
      elif args.diagnostic:
        correct += 1
  
  print "Classification rate: %.02f" % (float(classified) / len(listings))
  if args.diagnostic:
    print "Total listings: %d" % len(listings)
    print "Total classified: %d" % classified
    print "Correct: %d (%.02f)" % (correct, (float(correct) / len(listings)))
    print "Positive errors: %d (%.02f)" % (positive_error, (float(positive_error) / len(listings)))
    print "Negative errors: %d (%.02f)" % (negative_error, (float(negative_error) / len(listings)))

  # Process results dictionary into array of Result objects.
  processed_results = []
  for (product_name, classified_listings) in results.items():
    processed_results.append({
      'product_name' : product_name,
      'listings' : classified_listings
    })

  # Print results to "results.txt".
  print_results("results.txt", processed_results)

if __name__ == "__main__":
  main()
