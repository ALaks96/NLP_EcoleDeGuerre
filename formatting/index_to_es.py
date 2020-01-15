import os
from elasticsearch import Elasticsearch
from data.data_extractor import ppt_extractor, pdf_extractor, txt_extractor, docx_extractor, img_extractor, get_arbo
from formatting.contruct_database import to_json
#Initialise la connexion a ES avec les paremetres par defaut => localhost:9200
es = Elasticsearch()

def index_doc(location, save=False):
    paths = get_arbo(location)
    new_doc = {}

    for path in paths:

        filename = os.path.basename(path)
        print(filename)  
        new_doc["title"] = filename
        new_doc["filepath"] = path
        new_doc["isClassified"] = "No"
        if path.endswith(".pptx") or path.endswith(".ppt"):
            new_doc["author"], new_doc["data"], new_doc["preprocessed"] = ppt_extractor(path)
        elif path.endswith(".pdf"):
            new_doc["isClassified"], new_doc["author"], new_doc["data"], new_doc["preprocessed"] = pdf_extractor(path)
        elif path.endswith(".docx"):
            new_doc["author"], new_doc["data"], new_doc["preprocessed"] = docx_extractor(path)
        elif path.endswith(".docx"):
            new_doc["author"], new_doc["data"], new_doc["preprocessed"] = txt_extractor(path)
        elif path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg"):
            new_doc["author"], new_doc["data"], new_doc["preprocessed"] = "Image", img_extractor(path), None
        else:
            continue

        if save:
            to_json(new_doc, "index.json")
        else:
            continue

        # Envoi du document sur Elastic Search
        res = es.index(index="test", body=new_doc)
        print(res['result'] + " in ElasticSearch\n-------------------")
        new_doc = {}

    return True