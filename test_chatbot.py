import unittest
from chatbot import get_response


class test_chatbot(unittest.TestCase):
    def test_response(self):
        sentences = ["Hi", "Hello", "How are you?", "Search hello"]
        for sentence in sentences:
            assert get_response(sentence)


if __name__ == "__main__":
    unittest.main()
