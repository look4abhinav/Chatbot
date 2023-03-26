from chatbot import get_response


def test_response():
    sentences = ["Hi", "Hello", "How are you?", "Search hello"]
    for sentence in sentences:
        assert get_response(sentence)
