import PyPDF2
import textract
import os
import zipfile
import slate3k as slate
from pptx import Presentation
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from preprocessing.pre_processing import fix_text
from preprocessing.pre_processing import preprocessing
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import lxml.etree

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def pdf_extractor(path):
    # Open the pdf file in read binary mode.
    file_object = open(path, 'rb')

    # Create a pdf reader .
    pdf_file_reader = PyPDF2.PdfFileReader(file_object)

    try:
        creator = pdf_file_reader.getDocumentInfo()["/Author"]
    except:
        creator = "Unknown"

    current_page_number = 1
    paragraph_repo = {}
    #clean_paragraph_repo = {}
    Classified = "No"

    # Reliably retrieve text from pdf
    with open(path, 'rb') as f:
        doc = slate.PDF(f)
    # Loop in all the pdf pages.
    for page in doc:
        # Get pdf page text.
        temp1 = None
        #temp2 = None
        temp1 = page
        #temp2 = preprocessing(page)
        paragraph_repo[str(current_page_number)] = temp1
        #clean_paragraph_repo[str(current_page_number)] = temp2

        # if "cid" in temp2:
        #     c = 0
        #     c = temp2.count("cid")
        #
        #     if c > 5:
        #         Classified = "Yes"

        if not paragraph_repo[str(current_page_number)]:
            # If can not extract text then use ocr lib to extract the scanned pdf file.
            try:
                paragraph_repo[str(current_page_number)] = fix_text(textract.process(path,
                                                                                     method='tesseract',
                                                                                     encoding='utf-8'))
            except TimeoutError:
                continue

        current_page_number += 1

    return Classified, creator, paragraph_repo#, clean_paragraph_repo


def docx_extractor(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    ## GET METADATA
    # use lxml to parse the xml file we are interested in
    try:
        doc = lxml.etree.fromstring(document.read('docProps/core.xml'))
        # retrieve creator
        ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
        creator = doc.xpath('//dc:creator', namespaces=ns)[0].text
    except:
        creator = "Unknown"
    document.close()
    tree = XML(xml_content)

    doc = {}
    #clean_doc = {}
    paragraph_nb = 1
    for paragraph in tree.getiterator(PARA):
        texts = None
        text = ""
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            text = ''.join(texts)
            doc[str(paragraph_nb)] = fix_text(text)
            #clean_doc[str(paragraph_nb)] = preprocessing(text)
            paragraph_nb += 1

    return creator, doc#, clean_doc


def ppt_extractor(path):
    filename = os.path.basename(path)
    paragraph_repo = {}
    #@clean_paragraph_repo = {}
    f = open(path, "rb")
    prs = Presentation(f)
    slide_nb = 0
    if filename.endswith(".pptx"):
        try:
            document = zipfile.ZipFile(path)
            ## GET METADATA
            # use lxml to parse the xml file we are interested in
            doc = lxml.etree.fromstring(document.read('docProps/core.xml'))
            # retrieve creator
            ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
            creator = doc.xpath('//dc:creator', namespaces=ns)[0].text
        except:
            creator = "Unknown"
    else:
        creator = "Unknown"

    for slide in prs.slides:

        slide_nb += 1
        temp_text = ''

        for shape in slide.shapes:

            if hasattr(shape, "text") and shape.text.strip():
                temp_text += shape.text

        paragraph_repo[str(slide_nb)] = fix_text(temp_text)
        #clean_paragraph_repo[str(slide_nb)] = preprocessing(temp_text)

    return creator, paragraph_repo#, clean_paragraph_repo


def txt_extractor(path):
    doc = {}
    #clean_doc = {}
    paragraph_nb = 1

    with open(path) as f:
        lines = f.read()

    texts = lines.strip().split("/n/n")
    for text in texts:
        doc[str(paragraph_nb)] = fix_text(text)
        #clean_doc[str(paragraph_nb)] = preprocessing(text)
        paragraph_nb += 1

    return doc#, clean_doc


def img_extractor(path):
    parser = createParser(path)
    metadata = extractMetadata(parser)

    return metadata.exportDictionary()["Metadata"]


def get_arbo(location):
    # Initialize list of directories
    paths = []

    for file in os.listdir(location):
        path = str(location) + "/" + str(file)
        paths.append(path)

    return paths


def pdf_extractor2(path):
    # Open the pdf file in read binary mode.
    file_object = open(path, 'rb')

    # Create a pdf reader .
    pdf_file_reader = PyPDF2.PdfFileReader(file_object)

    try:
        creator = pdf_file_reader.getDocumentInfo()["/Author"]
    except:
        creator = "Unknown"

    # Get total pdf page number.
    total_page_number = pdf_file_reader.numPages

    current_page_number = 1
    paragraph_repo = {}
    #clean_paragraph_repo = {}
    Classified = "No"

    # Loop in all the pdf pages.
    while current_page_number < total_page_number:
        # Get the specified pdf page object.
        pdf_page = pdf_file_reader.getPage(current_page_number)
        text = pdf_page.extractText()
        #clean_text = preprocessing(text)

        # Get pdf page text.
        paragraph_repo[str(current_page_number)] = text
        #clean_paragraph_repo[str(current_page_number)] = clean_text

        # Process next page.
        current_page_number += 1

    if not paragraph_repo:
        # If can not extract text then use ocr lib to extract the scanned pdf file.
        paragraph_repo[str(current_page_number)] = textract.process(path, method='tesseract', encoding='utf-8')

    return Classified, creator, paragraph_repo#, clean_paragraph_repo


def pdf_extractor3(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    creator = "Unknown"

    current_page_number = 1
    paragraph_repo = {}
    #clean_paragraph_repo = {}
    Classified = "No"

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()
        #clean_text = preprocessing(text)
        paragraph_repo[str(current_page_number)] = text
        #clean_paragraph_repo[str(current_page_number)] = clean_text
        current_page_number += 1

    fp.close()
    device.close()
    retstr.close()
    return Classified, creator, paragraph_repo#, clean_paragraph_repo
