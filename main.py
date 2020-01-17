import os
import sys
from formatting.contruct_database import extract_text2, extract_text
from visualization.tree_graph import render_tree
from formatting.index_to_es import index_doc
# from connectdb import upload_to_es


location = os.getcwd() + "/data/data"
try:
    vectors = sys.argv[1]
    vectors = True
except IndexError:
    vectors = False

if vectors:
    print("Also fetching vector representations, re-arrange code and uncomment embedding import")
    texts = extract_text(location)
else:
    index_doc(location, save=True)

# index_doc(location, save=True)
# render_tree(location)