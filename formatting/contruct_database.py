import json
import os
from data.data_extractor import ppt_extractor
from data.data_extractor import pdf_extractor
from data.data_extractor import txt_extractor
from data.data_extractor import docx_extractor
from data.data_extractor import img_extractor
from data.data_extractor import get_arbo
from preprocessing.pre_processing import preprocessing


def to_json(dic, file_name="extracted_texts.json"):
    js = json.dumps(dic, indent=1)

    # Open new json file if not exist it will create
    fp = open(os.getcwd() + '/data/data/' + str(file_name), 'w')

    # write to json file
    fp.write(js)

    # close the connection
    fp.close()


def extract_text(location):
    paths = get_arbo(location)
    index = 0
    mega_dic = {}

    for path in paths:
        new_doc = {}
        filename = os.path.basename(path)
        print(filename)
        new_doc["title"] = filename
        new_doc["filepath"] = path
        new_doc["isClassified"] = "No"
        new_doc['author'] = "Unknown"
        if path.endswith(".pptx") or path.endswith(".ppt"):
            new_doc['author'], \
            new_doc["data"], \
            new_doc["preprocessed"] = ppt_extractor(path)
            index += 1
            mega_dic[str(index)] = new_doc
        elif path.endswith(".pdf"):
            new_doc["isClassified"], \
            new_doc["author"], \
            new_doc["data"], \
            new_doc["preprocessed"] = pdf_extractor(path)
            index += 1
            mega_dic[str(index)] = new_doc
        elif path.endswith(".docx"):
            new_doc["author"], \
            new_doc["data"], \
            new_doc["preprocessed"] = docx_extractor(path)
            index += 1
            mega_dic[str(index)] = new_doc
        elif path.endswith(".docx"):
            new_doc["author"], \
            new_doc["data"], \
            new_doc["preprocessed"] = txt_extractor(path)
            index += 1
            mega_dic[str(index)] = new_doc
        elif path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg"):
            new_doc["data"], \
            new_doc["preprocessed"] = img_extractor(path), None
            index += 1
            mega_dic[str(index)] = new_doc
        else:
            continue

    to_json(mega_dic)

    return mega_dic


def launch_preprocessing(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = launch_preprocessing(v)

        else:
            d[k] = preprocessing(v)

    return d
