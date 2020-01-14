import os
from formatting.contruct_database import extract_text
from formatting.contruct_database import launch_preprocessing
from visualization.tree_graph import render_tree

location = os.getcwd() + "/data/data"
render_tree(location)
texts = extract_text(location)
texts_nlp = launch_preprocessing(texts)