import string
import unidecode
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from ftfy import fix_encoding


def requirements():

    try:
        stopword_list = stopwords.words('english')

    except OSError:
        nltk.download('stopwords')
        stopword_list = stopwords.words('english')

    try:
        lemmatizer = WordNetLemmatizer()

    except OSError:
        nltk.download('wordnet')
        lemmatizer = WordNetLemmatizer()

    special_characters = ["@", "/", "#", ".", ",", "!", "?", "(", ")", "-", "_", "’", "'", "\"", ":", "=", "+", "&",
                          "`", "*", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "'", '.', '‘', ';']

    transformation_sc_dict = {initial: " " for initial in special_characters}

    return stopword_list, lemmatizer, transformation_sc_dict


def clean_text(text):

    # convert text to lowercase
    text = text.strip().lower()

    # replace punctuation characters with spaces
    filters = '"\'%&()*,-./:;<=>?[\\]^_`{|}~\t\n'
    translate_dict = dict((c, " ") for c in filters)
    translate_map = str.maketrans(translate_dict)
    text = text.translate(translate_map)

    return text


def correct_ascii(text):
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))

    return text


def fix_text(text):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\u2013", "-")
    text = text.replace("\u03d5", "ϕ")
    text = text.rstrip("\n")
    text = text.rstrip("\t")
    text = fix_encoding(text)
    text = unidecode.unidecode(text)
    text = correct_ascii(text)

    return text


def concat_str_list(l):
    s = ' '.join(l)

    return s


def preprocessing(text):

    stopword_list, lemmatizer, transformation_sc_dict = requirements()

    # Tokenization
    tokens = word_tokenize(text)

    # Deleting words with  only one character
    tokens = [token for token in tokens if len(token) > 0]

    # stopwords + lowercase
    tokens = [token.lower() for token in tokens if token.lower() not in stopword_list]

    # Deleting specific characters
    tokens = [token.translate(str.maketrans(transformation_sc_dict)) for token in tokens]

    # Lemmatizing tokens
    tokens = [lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(token, pos='a'), pos='v'), pos='n') for
              token in tokens]

    # Final cleaning of additionnal characters
    tokens = [clean_text(token) for token in tokens]

    return concat_str_list(tokens)
