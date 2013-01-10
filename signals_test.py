import unittest
from signals import contains_subsequence, model_name_signal, manufacturer_name_signal, merge_tokens, tokenize

class TestSignals(unittest.TestCase):
        
    def test_tokenize(self):
      self.assertEqual(tokenize("a b c"), ["a", "b", "c"])
      self.assertEqual(tokenize("a b  c"), ["a", "b", "c"])
      self.assertEqual(tokenize("a DMC b c"), ["a", "b", "c"])
      self.assertEqual(tokenize("a b DSC c"), ["a", "b", "c"])
      self.assertEqual(tokenize("IS a DMC-b c"), ["a", "b", "c"])
        
    def test_merge_tokens(self):
      self.assertEqual(merge_tokens(["a", "b", "c"], 0), ["ab", "c"])
      self.assertEqual(merge_tokens(["a", "b", "c"], 1), ["a", "bc"])
        
    def test_contains_subsequence(self):
      self.assertEqual(contains_subsequence([1, 2, 3], []), (0, 0))
      self.assertEqual(contains_subsequence([1, 2, 3], [1]), (0, 1))
      self.assertEqual(contains_subsequence([1, 2, 3], [1, 2]), (0, 2))
      self.assertEqual(contains_subsequence([1, 2, 3], [2, 3]), (1, 2))
      self.assertEqual(contains_subsequence([1, 2, 3], [3]), (2, 1))
      self.assertEqual(contains_subsequence([1, 2, 3], [3, 4]), (-1, 0))
      self.assertEqual(contains_subsequence([1, 2, 3], [1, 3]), (-1, 0))
      self.assertEqual(contains_subsequence([], []), (0, 0))
      self.assertEqual(contains_subsequence([], [1]), (-1, 0))
      self.assertEqual(contains_subsequence(['title'], ['title']), (0, 1))
      
    def test_model_name_signal(self):
      self.assertEqual(1,
          model_name_signal({ "model" : "TITLE" }, { "title" : "TITLE" }))
      self.assertEqual(1,
          model_name_signal({ "model" : "TITLE" }, { "title" : "TITLE FOO" }))
      self.assertEqual(1,
          model_name_signal({ "model" : "title" }, { "title" : "FOO TITLE BAR" }))
      self.assertEqual(2,
          model_name_signal({ "model" : "TITLE 2" }, { "title" : "FOO title 2 BAR" }))
      self.assertEqual(1,
          model_name_signal({ "model" : "TITLE FOO" }, { "title" : "BAR TITLEFOO BAR" }))    
      
      self.assertEqual(0, model_name_signal({ "model" : "TITLE FOO" }, { "title" : "TITLE" }))
      self.assertEqual(0, model_name_signal({ "model" : "FOO TITLE" }, { "title" : "TITLE BAR" }))
      self.assertEqual(0, model_name_signal({ "model" : "foo TITLE bar" }, { "title" : "TITLE 2" }))
      self.assertEqual(0, model_name_signal({ "model" : "TITL" }, { "title" : "TITLE" }))
    
    def test_manufacturer_name_signal(self):
      self.assertEqual(0,
          manufacturer_name_signal({"manufacturer" : "foo"}, {"manufacturer" : "bar"}))
      self.assertEqual(1,
          manufacturer_name_signal({"manufacturer" : "foo"}, {"manufacturer" : "foo"}))
      self.assertEqual(1,
          manufacturer_name_signal({"manufacturer" : "foo"}, {"manufacturer" : "foo bar"}))

if __name__ == '__main__':
    unittest.main()