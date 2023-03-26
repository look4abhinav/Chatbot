#!/usr/bin/env python

__author__ = "Abhinav Srivastava"
__version__ = "1.0"


import json
import pickle

import keras
import nltk
from keras.layers import Dense, Dropout
from nltk.stem import PorterStemmer


def preprocess_data(intents: dict) -> list[list]:
    words, tags, documents = [], [], []
    punctuations = ("!", "@", "#", ".", ",", "?", ";")

    stemmer = PorterStemmer()
    for intent in intents["intents"]:
        tag = intent["tag"]
        for sentence in intent["patterns"]:
            tokens = [
                stemmer.stem(word=token, to_lowercase=True)
                for token in nltk.word_tokenize(sentence)
                if token not in punctuations
            ]
            words.extend(token for token in tokens)
            documents.append((tag, tokens))
        tags.append(tag)

    bag_of_words, bag_of_tags = [], []
    tags_count = len(tags)
    for tag, tokens in documents:
        word_row = []
        tag_row = [0] * tags_count
        for word in words:
            word_row.append(1) if word in tokens else word_row.append(0)
        tag_row[tags.index(tag)] = 1
        bag_of_words.append(word_row)
        bag_of_tags.append(tag_row)

    print("Writing Pickle files...")
    with open("words.pkl", "wb") as f:
        pickle.dump(words, f)
    with open("tags.pkl", "wb") as f:
        pickle.dump(tags, f)
    return bag_of_words, bag_of_tags


def train_model(x: list[list], y: list[list]) -> keras.Model:

    model = keras.Sequential()
    model.add(Dense(units=128, activation="relu", input_shape=(len(x[0]),)))
    model.add(Dropout(0.5))
    model.add(Dense(units=64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(units=len(y[0]), activation="softmax"))

    sgd = keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    stop_early = keras.callbacks.EarlyStopping(monitor="accuracy", patience=5)

    model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
    model.fit(
        x,
        y,
        epochs=500,
        batch_size=3,
        verbose=0,
        shuffle=True,
        workers=3,
        use_multiprocessing=True,
        callbacks=[stop_early],
    )
    accuracy = model.evaluate(x, y, verbose=0, use_multiprocessing=True)[1]

    print(f"Model Accuracy: {accuracy*100:.2f}%\nSaving model...")
    model.save("model.h5")
    return model


if __name__ == "__main__":

    path = "trainingdata.json"
    with open(path, "r") as js:
        intents = json.load(js)

    x, y = preprocess_data(intents)
    model = train_model(x, y)
