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

    js = json.dumps(dic)

    # Open new json file if not exist it will create
    fp = open(os.getcwd() + '/data/data/' + str(file_name), 'a')

    # write to json file
    fp.write(js)

    # close the connection
    fp.close()


def extract_text(location):
    paths = get_arbo(location)
    texts = {}
    index = 0
    mega_dic = {}

    for path in paths:

        filename = os.path.basename(path)

        if path.endswith(".pptx") or path.endswith(".ppt"):
            print(index)
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["filepath"] = path
            texts["isClassified"] = "No"
            texts['author'], texts["data"] = ppt_extractor(path)
            index += 1
            mega_dic[str(index)] = texts
            texts = {}

        if path.endswith(".pdf"):
            print(index)
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["filepath"] = path
            texts["isClassified"] = "No"
            texts["author"], texts["data"] = pdf_extractor(path)
            mega_dic[str(index)] = texts
            index += 1
            texts = {}

        if path.endswith(".docx"):
            print(index)
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["filepath"] = path
            texts["isClassified"] = "No"
            texts["author"], texts["data"] = docx_extractor(path)
            index += 1
            mega_dic[str(index)] = texts
            texts = {}

        if path.endswith(".txt"):
            print(index)
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["filepath"] = path
            texts["isClassified"] = "No"
            texts['author'], texts["data"] = "Unknown", txt_extractor(path)
            index += 1
            mega_dic[str(index)] = texts
            texts = {}

        if path.endswith(".png") or path.endswith(".jpg"):
            print(index)
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["filepath"] = path
            texts["isClassified"] = "No"
            texts['author'], texts["data"] = "Unknown", img_extractor(path)
            index += 1
            mega_dic[str(index)] = texts
            texts = {}

    to_json(mega_dic)

    return mega_dic


def launch_preprocessing(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = launch_preprocessing(v)

        else:
            d[k] = preprocessing(v)

    return d
