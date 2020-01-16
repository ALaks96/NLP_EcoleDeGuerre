import os
import fasttext.util
import numpy as np
from gensim.models import KeyedVectors
from preprocessing.pre_processing import preprocessing

path_to_w2v_en = os.getcwd() + "/data/data/GoogleNews-vectors-negative300.bin"
path_to_w2v_fr = os.getcwd() + "/data/data/cc.co.300.bin"

print("getting french google word2vec")
w2v_fr = fasttext.load_model(path_to_w2v_fr)
print("done")

print("getting english google word2vec")
w2v_en = KeyedVectors.load_word2vec_format(path_to_w2v_en, binary=True)
print("done")


def vectorizer(text, lang="en"):
    """Identify the vector values for each word in the given document"""
    text = preprocessing(text)
    word_vecs = []
    words = text.split(" ")
    for word in words:
        try:
            if lang == 'en':
                vec = w2v_en[word]
            else:
                vec = w2v_fr[word]
            word_vecs.append(vec)
        except KeyError:
            # Ignore if the word doesn't exist in the vocabulary
            pass

    # Assuming that document vector is the mean of all the word vectors
    vector = np.mean(word_vecs, axis=0).tolist()
    return vector