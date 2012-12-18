from data import get_data, print_results
from classifier import Classifier
from collections import defaultdict

def main():
  # Load data from files.
  listings = get_data("listings.txt")
  products = get_data("products.txt")

  # Create a classifier for the provided products.
  classifier = Classifier(products)

  # Classify all listings.
  results = defaultdict(list)
  classified = 0
  for listing in listings:
    product_name = classifier.classify(listing)
    if product_name is not None:
      classified += 1
      results[product_name].append(listing)
  
  print "Classification rate: %.02f" % (float(classified) / len(listings))

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
