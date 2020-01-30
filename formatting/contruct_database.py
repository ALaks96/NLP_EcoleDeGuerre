import json
import os
from data.data_extractor import ppt_extractor
from data.data_extractor import pdf_extractor3
from data.data_extractor import txt_extractor
from data.data_extractor import docx_extractor
from data.data_extractor import img_extractor
from data.data_extractor import excel_extractor
from data.data_extractor import scan_extractor
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
        new_doc["isClassified"] = False
        new_doc['author'] = "Unknown"
        if path.endswith(".pptx") or path.endswith(".ppt"):
            try:
                new_doc['author'], \
                new_doc["data"], \
                new_doc["vectors"] = ppt_extractor(path, vectors=True)
                index += 1
                mega_dic[str(index)] = new_doc
            except:
                pass
        elif path.endswith(".pdf"):
            try:
                new_doc["isClassified"], \
                new_doc["author"], \
                new_doc["data"], \
                new_doc["vectors"] = pdf_extractor3(path, vectors=True)
                index += 1
                mega_dic[str(index)] = new_doc
            except:
                try:
                    new_doc["data"], \
                    new_doc["vectors"] = scan_extractor(path, vectors=True)
                except:
                    pass
        elif path.endswith(".docx"):
            try:
                new_doc["author"], \
                new_doc["data"], \
                new_doc["vectors"] = docx_extractor(path, vectors=True)
                index += 1
                mega_dic[str(index)] = new_doc
            except:
                pass
        elif path.endswith(".txt"):
            try:
                new_doc["author"], \
                new_doc["data"], \
                new_doc["vectors"] = txt_extractor(path, vectors=True)
                index += 1
                mega_dic[str(index)] = new_doc
            except:
                pass
        elif path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg"):
            try:
                new_doc["data"], \
                new_doc["vectors"] = img_extractor(path), None
                index += 1
                mega_dic[str(index)] = new_doc
            except:
                pass
        elif path.endswith(".xls") or path.endswith(".xlsx"):
            try:
                new_doc["data"], \
                new_doc["vectors"] = excel_extractor(path)
                index += 1
                mega_dic[str(index)] = new_doc
            except:
                pass
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


def extract_text2(location):
    paths = get_arbo(location)
    index = 0
    mega_dic = {}

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
                index += 1
                mega_dic[str(index)] = new_doc
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".pdf"):
            try:
                new_doc["isClassified"], \
                new_doc["author"], \
                new_doc["data"] = pdf_extractor3(path)
                index += 1
                mega_dic[str(index)] = new_doc
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".docx"):
            try:
                new_doc["author"], \
                new_doc["data"] = docx_extractor(path)
                index += 1
                mega_dic[str(index)] = new_doc
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".docx"):
            try:
                new_doc["author"], \
                new_doc["data"] = txt_extractor(path)
                index += 1
                mega_dic[str(index)] = new_doc
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg"):
            try:
                new_doc["data"] = img_extractor(path)
                index += 1
                mega_dic[str(index)] = new_doc
            except Exception as e:
                print(e)
                pass
        elif path.endswith(".xls") or path.endswith(".xlsx"):
            try:
                new_doc["author"], \
                new_doc["data"] = excel_extractor(path)
                index += 1
                mega_dic[str(index)] = new_doc
            except Exception as e:
                print(e)
                pass
        else:
            continue

    to_json(mega_dic)

    return mega_dic
