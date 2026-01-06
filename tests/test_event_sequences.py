"""
Tests the parser for : given any string, return a list of E\d+ tokens.
"""


import unittest
from aiops_hdfs.data.event_sequences import extract_event_tokens

class TestEventParsing(unittest.TestCase):
    def test_basic_space_seperated(self):
        self.assertEqual(extract_event_tokens("E1 E2 E3"), ["E1", "E2", "E3"])

    def test_list_like_string(self):
        self.assertEqual(extract_event_tokens("['E10','E2','E2']"), ["E10", "E2", "E2"])
    
    def test_mixed_noise(self):
        # Testing for messy format since real logs are usually messy!
        s = "INFO something E7, else [E8] end E9"
        self.assertEqual(extract_event_tokens(s), ["E7", "E8", "E9"])

    def test_empty(self):
        self.assertEqual(extract_event_tokens(""), [])
        self.assertEqual(extract_event_tokens("   "), [])
        self.assertEqual(extract_event_tokens(None), [])


if __name__ == "__main__":
    unittest.main()