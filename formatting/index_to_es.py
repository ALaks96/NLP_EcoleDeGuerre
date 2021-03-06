import os, json
from elasticsearch import Elasticsearch
from data.data_extractor import ppt_extractor, pdf_extractor, pdf_extractor2, pdf_extractor3, txt_extractor, docx_extractor, img_extractor, get_arbo, excel_extractor

#Initialise la connexion a ES avec les paremetres par defaut => localhost:9200
es = Elasticsearch()

def get_paths():
    l = []
    with open(os.getcwd() + '/scan.json') as json_file:
        data = json.load(json_file)
    for p in data:
        if(p['type'] in ['docx', 'doc', 'ppt', 'pptx', 'xslx', 'pptx', 'pdf', 'txt', 'png', 'jpg', 'jpeg']):
            l.append(p['filepath'])
    return l

def index_doc(location, save=False):
    paths = get_paths()

    for path in paths:
        new_doc = {}
        filename = os.path.basename(path)
        print(filename)
        new_doc["title"] = filename
        new_doc["filepath"] = path
        new_doc["isClassified"] = False
        new_doc['author'] = "Unknown"
        if path.endswith(".pptx") or path.endswith(".ppt"):
            try:
                new_doc['author'], \
                new_doc["data"] = ppt_extractor(path)
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".pdf"):
            try:
                new_doc["isClassified"], \
                new_doc["author"], \
                new_doc["data"] = pdf_extractor3(path)

            except Exception as e:
                print(e)
                pass
        elif path.endswith(".docx"):
            try:
                new_doc["author"], \
                new_doc["data"] = docx_extractor(path)
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".docx"):
            try:
                new_doc["author"], \
                new_doc["data"] = txt_extractor(path)
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg"):
            try:
                new_doc["data"] = img_extractor(path)
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".xls") or path.endswith(".xlsx"):
            try:
                new_doc["author"], \
                new_doc["data"] = excel_extractor(path)
            except Exception as e:
                print(e)
                pass
        else:
            continue

        if save:
            to_json(new_doc, "index.json")

        # Envoi du document sur Elastic Search
        res = es.index(index="test2", body=new_doc)
        print(res['result'] + " in ElasticSearch\n-------------------")
        new_doc = {}

    return True

def to_json(dic, file_name="extracted_texts.json"):
    js = json.dumps(dic, indent=1)
    # Open with append option 'a'
    fp = open(os.getcwd() + '/data' + str(file_name), 'a')
    fp.write(js)
    fp.close()
