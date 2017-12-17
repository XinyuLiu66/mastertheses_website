from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import os
# from PyPDF2 import PdfFileReader
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfpage import PDFTextExtractionNotAllowed
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.layout import *
# from pdfminer.converter import PDFPageAggregator
import re

# ================================================================================= #
def parser_pdf_links(url):
    """
    Parser pdf links from google scholar of specific person
    one pdf is a document for the person
    :param url: a url in google scholar
    :return: links: a list of links
    """
    links = list()
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        print('HTTPError: ' + str(e.code))
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: ' + str(e.reason))
    response = urlopen(req)
    content = response.read()
    soup = BeautifulSoup(content, 'html.parser')
    # all the tags including pdf file
    pdf_tags = soup.find_all('div', class_='gs_or_ggsm')
    # parser pdf link
    for tag in pdf_tags:
        for child in tag.children:
            if child.name == 'a' and child['href'].endswith(".pdf"):
                links.append(child['href'])
                break
    return links

"""
# demo
url = "https://scholar.google.de/scholar?start=0&q=Johannes+F%C3%BCrnkranz&hl=de&as_sdt=0,5"
pdf_links = parser_pdf_links(url)
for i, link in enumerate(pdf_links):
    print("i = ", i, "   ", link)
"""

# ================================================================================= #
def parser_title_abstract(url):
    """
    get the title and abstract of each paper the author have published from google scholar
    :param url: the website of a specific person in google scholar
    :return: a list of dictionary, e.g [{title: , abstract: }, {}, ...]
    """
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup
    import urllib.request, urllib.error
    import re

    results = []
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        print('HTTPError: ' + str(e.code))
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: ' + str(e.reason))
    response = urlopen(req)
    content = response.read()
    soup = BeautifulSoup(content, 'html.parser')
    # all the tags including pdf file
    papers_tag = soup.find_all('div', class_='gs_ri')
    for tag in papers_tag:
        paper_info = dict()
        title = " "
        abstract = " "
        # and child.get('class') == 'gs_rt'
        for child in tag.children:
            if child.name == 'h3':
                title = child.string
                paper_info['title'] = title
            if child.name == 'div' and child['class'] == [u'gs_rs']:
                child_tag = str(child)
                cleanr = re.compile('<.*?>')
                abstract = re.sub(cleanr,'', child_tag)
                paper_info['abstract'] = abstract.replace('Abstract ',"")
        results.append(paper_info)
    return results

'''
# demo 1
url = "https://scholar.google.de/scholar?start=0&q=Johannes+F%C3%BCrnkranz&hl=de&as_sdt=0,5"
paper_info = parser_title_abstract(url)
for info in paper_info:
    print("=========")
    print(info)
'''
# ================================================================================= #




# demo 2
# TODO   umlaut
# def main(person_name ):
#     i = 0
#     first_name = person_name.split(' ')[0]
#     last_name = person_name.split(' ')[1]
#     url = "https://scholar.google.de/scholar?start="+str(i)+"&q="+first_name+"+"+last_name+"&hl=de&as_sdt=0,5"
#     count = 1
#     while i < 100:
#         try:
#             paper_info = parser_title_abstract(url)
#         except urllib.error.HTTPError as e:
#             # Return code error (e.g. 404, 501, ...)
#             print('HTTPError: ' + str(e.code))
#             break
#         except urllib.error.URLError as e:
#             # Not an HTTP-specific error (e.g. connection refused)
#             # ...
#             print('URLError: ' + str(e.reason))
#             break
#         for info in paper_info:
#             print("=========   ", "Count = ", count)
#             print(info)
#             count += 1
#         i += 10
#
# main("Jan Peters")
# ================================================================================= #
def download_pdf(directory, pdf_links):
    """
    download pdf file of given link to the directory
    :param pdf_links: a collection of pdf link
    :return: none
    """
    # create a directory of this person
    if not os.path.exists(directory):
        os.mkdir(directory)
    # download pdf file into this directory
    for link in pdf_links:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        file_name = link.split('/')[-1]
        file_path = os.path.join(directory, file_name)
        if not os.path.isfile(file_path):
            file = open(file_path, 'wb')
            file.write(response.read())
            file.close()

"""
# demo
url = "https://scholar.google.de/scholar?start=0&q=Johannes+F%C3%BCrnkranz&hl=de&as_sdt=0,5"
pdf_links = parser_pdf_links(url)
directory = "JF"
download_pdf(directory, pdf_links)

"""
# ================================================================================= #

"""
# This method is cool, but not very efficient and practical

def parser_doc_data(directory):

    # parser title, abstract and key words from each document in directory using pdfMiner and pyPDF library
    # :param directory: a directory includes a collection of papers
    # :return: a list of dictionary, e.g [{title: , abstract: , keywords: }, {}, ...]
    #
    papar_datas = list()
    files = os.listdir(directory)
    for file in files:
        text = []
        file = os.path.join(directory, file)
        with open(file, 'rb') as f:
            parser = PDFParser(f)
            document = PDFDocument(parser)
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            # set a resource manager
            rsrcmgr = PDFResourceManager(caching=False)
            # set a equipment
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # set a interpreter
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            replace = re.compile(r'\s+')
            # all the page object
            pages = PDFPage.create_pages(document)
            # title, abstract, key words information is in the first page, so only parser page 0
            interpreter.process_page(list(pages)[0])
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):   # if x is a text data
                    temp_text = re.sub(replace, ' ', x.get_text())
                    if (len(temp_text)) != 0:
                        text.append(temp_text)
            # get title, abstract, key words
            dic_paper_info = {}
            # get title
            pdf_reader = PdfFileReader(f)
            title = pdf_reader.getDocumentInfo().title
            dic_paper_info['title'] = title
            # get abstract and key words data
            abstract = ""
            key_words = ""
            for i, t in enumerate(text):
                if t.startswith('Abstract'):
                    if t.endswith('Abstract'):
                        abstract = text[i + 1]
                        continue
                    else:
                        abstract = t
                        continue
                elif t.startswith('Key'):
                    key_words = t
                    continue
            dic_paper_info['abstract'] = abstract
            dic_paper_info['key_words'] = key_words

            papar_datas.append(dic_paper_info)
    return papar_datas

"""






