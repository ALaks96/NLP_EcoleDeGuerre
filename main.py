import os
from formatting.contruct_database import extract_text
from formatting.contruct_database import launch_preprocessing
from visualization.tree_graph import render_tree
from formatting.index_to_es import index_doc

location = os.getcwd() + "/data/data"
#render_tree(location)
index_doc(location)
#texts_nlp = launch_preprocessing(texts)