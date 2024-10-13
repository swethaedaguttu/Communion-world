# tests/test_ai_features.py

import unittest
from features.ai_features import ai_assistant_query

class TestAI(unittest.TestCase):
    def test_ai_response_hello(self):
        response = ai_assistant_query("hello")
        self.assertEqual(response, "Hello! How can I assist you today?")

    def test_ai_response_help(self):
        response = ai_assistant_query("help")
        self.assertEqual(response, "Sure! What do you need help with?")

    def test_ai_response_unknown(self):
        response = ai_assistant_query("unknown")
        self.assertEqual(response, "I'm sorry, I didn't understand that.")

if __name__ == "__main__":
    unittest.main()
