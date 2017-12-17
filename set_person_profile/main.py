import sys
sys.path.append("..")
from mastertheses.set_person_profile.set_person_corpus.set_person_corpus import *
from mastertheses.set_person_profile.wordnet_KP_extractor.wordnet_method import *

html = "https://scholar.google.de/scholar?start=0&q=Johannes+F%C3%BCrnkranz&hl=de&as_sdt=0,5"

dic_doc = parser_title_abstract(html)

def get_profile(dic_doc):
    for doc in dic_doc:
        doc_title = doc.get('title')
        doc_abstract = doc.get('abstract')
        if doc_title:
            if doc_abstract:
                doc_text = doc_title + "," + doc_abstract
            else:
                doc_text = doc_title
        else:
            if doc_abstract:
                doc_text = doc_abstract
            else:
                doc_text = None
        KP = score_keyphrases_by_textrank(doc_text, doc_title,n_keywords=0.5)
        print(KP)
        print(" ==========  ")
get_profile(dic_doc)