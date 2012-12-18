from collections import defaultdict
import signals
import pprint

AMBIGUITY_THRESHOLD = 5

class Classifier(object):
  def __init__(self, products):
    self.products = products
    self.name_to_product = {}
    for product in products:
      self.name_to_product[product["product_name"]] = product
    self.all_signals = {
      "name" : signals.model_name_signal,
      "manufacturer" : signals.manufacturer_name_signal,
      "family" : signals.family_signal
    }
    self.pp = pprint.PrettyPrinter(indent=2, depth=4)

  # Returns True if signal_result represents a candidate.
  def evaluate_signals(self, results):
    if results["name"] and results["manufacturer"]:
      return results["name"] + (1 if results["family"] else 0)

  # Returns the product name that most closely matches listing. If two products closely match, or
  # there are no close matches, returns None.
  def classify(self, listing):
    best_ranking = -1
    best_candidates = []
    name_to_signals = {}
    for product in self.products:
      signal_results = {}
      for (signal_name, signal) in self.all_signals.items():
        signal_results[signal_name] = signal(product, listing)
      ranking = self.evaluate_signals(signal_results)
      if ranking > 0:
        name_to_signals[product["product_name"]] = signal_results
        if ranking > best_ranking:
          best_candidates = [product]
          best_ranking = ranking
        elif ranking == best_ranking:
          best_candidates.append(product)

    if len(best_candidates) == 0:
      print "Failed on %s, because there were no candidates\n" % (str(listing))
      return None
    elif len(best_candidates) == 1:
      return best_candidates[0]["product_name"]
    else:
      print "Failed on %s, because there were at least two plausible candidates:\n%s\n  It scored: %s\n%s\n  It scored: %s\n" % (
          str(listing),
          self.pp.pformat(best_candidates[0]), str(name_to_signals[best_candidates[0]["product_name"]]),
          self.pp.pformat(best_candidates[1]), str(name_to_signals[best_candidates[1]["product_name"]])
      )
      return None
