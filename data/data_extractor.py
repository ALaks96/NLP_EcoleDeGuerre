import json
import os
import PyPDF2
import textract
from pptx import Presentation
from ftfy import fix_encoding

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def get_arbo(location):
    # Initialize list of directories
    paths = []

    for file in os.listdir(location):
        path = str(location) + "/" + str(file)
        paths.append(path)

    return paths


def pdf_extractor(path):
    # Open the pdf file in read binary mode.
    file_object = open(path, 'rb')

    # Create a pdf reader .
    pdf_file_reader = PyPDF2.PdfFileReader(file_object)

    # Get total pdf page number.
    total_page_number = pdf_file_reader.numPages

    # Print pdf total page number.
    print('This pdf file contains totally ' + str(total_page_number) + ' pages.')

    current_page_number = 1
    paragraph_repo = {}

    # Loop in all the pdf pages.
    while current_page_number < total_page_number:
        # Get the specified pdf page object.
        pdf_page = pdf_file_reader.getPage(current_page_number)

        # Get pdf page text.
        paragraph_repo[str(current_page_number)] = pdf_page.extractText()

        # Process next page.
        current_page_number += 1

    if not paragraph_repo:
        # If can not extract text then use ocr lib to extract the scanned pdf file.
        paragraph_repo[str(current_page_number)] = fix_text(textract.process(path,
                                                                             method='tesseract',
                                                                             encoding='utf-8'))

    return paragraph_repo


def fix_text(text):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\u2013", "-")
    text = text.replace("\u03d5","ϕ")
    text = text.rstrip("\n")
    text = text.rstrip("\t")
    text = fix_encoding(text)

    return text


def docx_extractor(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    doc = {}
    paragraph_nb = 1
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            text = ''.join(texts)
            doc[str(paragraph_nb)] = fix_text(text)
            paragraph_nb += 1

    return doc


def ppt_extractor(path):
    paragraph_repo = {}
    f = open(path, "rb")
    prs = Presentation(f)

    slide_nb = 0
    temp_text = ''

    for slide in prs.slides:

        slide_nb += 1

        for shape in slide.shapes:

            if hasattr(shape, "text") and shape.text.strip():
                temp_text += shape.text

        paragraph_repo[str(slide_nb)] = fix_text(temp_text)

    return paragraph_repo


def txt_extractor(path):
    doc = {}
    paragraph_nb = 1

    with open(path) as f:
        lines = f.read()

    texts = lines.strip().split("/n/n")
    for text in texts:
        doc[str(paragraph_nb)] = fix_text(text)
        paragraph_nb += 1

    return doc


def to_json(dic):
    js = json.dumps(dic)

    # Open new json file if not exist it will create
    fp = open(os.getcwd() + '/data/data/extracted_texts.json', 'a')

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
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["data"] = ppt_extractor(path)
            index += 1
            mega_dic[str(index)] = texts
            print(index)
            texts = {}

        if path.endswith(".pdf"):
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["data"] = pdf_extractor(path)
            mega_dic[str(index)] = texts
            index += 1
            print(index)
            texts = {}

        if path.endswith(".docx"):
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["data"] = docx_extractor(path)
            index += 1
            mega_dic[str(index)] = texts
            print(index)
            texts = {}

        if path.endswith(".txt"):
            print(filename)
            print("----------------------")

            texts["title"] = filename
            texts["data"] = docx_extractor(path)
            index += 1
            mega_dic[str(index)] = texts
            print(index)
            texts = {}

    to_json(mega_dic)

    return mega_dic
