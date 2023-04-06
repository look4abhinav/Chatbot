import unittest
from chatbot import get_response


class test_chatbot(unittest.TestCase):
    def test_greeting(self):
        sentences = ["Hi", "Hello", "How are you?"]
        for sentence in sentences:
            assert get_response(sentence)

    def test_goodbye(self):
        sentences = ["Bye", "See you later", "Goodbye"]
        for sentence in sentences:
            assert get_response(sentence)

    def test_thanks(self):
        sentences = ["Thanks", "Thank you", "That's helpful"]
        for sentence in sentences:
            assert get_response(sentence)

    def test_thanks(self):
        sentences = ["Thanks", "Thank you", "That's helpful"]
        for sentence in sentences:
            assert get_response(sentence)

    def test_thanks(self):
        sentences = ["Tell me a joke", "joke", "Make me laugh"]
        for sentence in sentences:
            assert get_response(sentence)


if __name__ == "__main__":
    unittest.main()
