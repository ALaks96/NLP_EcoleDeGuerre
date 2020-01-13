import os
from data.data_extractor import extract_text

location = os.getcwd() + "/data/data/"
texts = extract_text(location)
