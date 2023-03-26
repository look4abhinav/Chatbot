#!/usr/bin/env python

__author__ = "Abhinav Srivastava"
__version__ = "1.0"


import json
import pickle
import random
from pathlib import Path

import nltk
from nltk.stem import PorterStemmer
from tensorflow import keras

output_path = Path.cwd() / "output"

with open(output_path / "words.pkl", "rb") as f:
    all_words = pickle.load(f)
with open(output_path / "tags.pkl", "rb") as f:
    labels = pickle.load(f)
with open("trainingdata.json", "r") as f:
    intents = json.load(f)

model = keras.models.load_model(output_path / "model.h5")
stemmer = PorterStemmer()


def preprocess(sentence: str) -> list[int]:
    words = [
        stemmer.stem(word, to_lowercase=True) for word in nltk.word_tokenize(sentence)
    ]
    bag_of_words = [0] * len(all_words)

    for i, word in enumerate(all_words):
        if word in words:
            bag_of_words[i] = 1

    return list(bag_of_words)


def get_response(sentence) -> str:
    bag_of_words = preprocess(sentence)
    predictions = list(model.predict([bag_of_words], verbose=0)[0])
    predicted = max(predictions)
    if predicted < 0.50:
        return "Sorry! I couldn't understand."
    label = labels[predictions.index(predicted)]
    for intent in intents["intents"]:
        if label == intent.get("tag"):
            return random.choice(intent.get("responses"))


if __name__ == "__main__":
    print("Bot Online")
    try:
        while True:
            sentence = input("You: ")
            response = get_response(sentence)
            print(f"Bot: {response}")
    except KeyboardInterrupt:
        print("\nBot Offline")
