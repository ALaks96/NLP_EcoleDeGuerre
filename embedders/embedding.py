import os
from gensim.models import KeyedVectors
from preprocessing.pre_processing import preprocessing
import numpy as np
path_to_w2v = os.getcwd() + "/data/data/"
print("getting google word2vec")
w2v = KeyedVectors.load_word2vec_format(path_to_w2v + 'GoogleNews-vectors-negative300.bin', binary=True)
print("done")


def vectorizer(text):
    """Identify the vector values for each word in the given document"""
    text = preprocessing(text)
    word_vecs = []
    words = text.split(" ")
    for word in words:
        try:
            vec = w2v[word]
            word_vecs.append(vec)
        except KeyError:
            # Ignore if the word doesn't exist in the vocabulary
            pass

    # Assuming that document vector is the mean of all the word vectors
    vector = np.mean(word_vecs, axis=0).tolist()
    return vector