
# ========================================= part 1 ===========================================================

def parser_title(url):
    """
    parser all the titles from DBLP
    :param url: a dblp url
    :return: titles, a list of title
    """
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup
    import  urllib.error


    titles = []   # results
    try:
        req = Request(url)
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
    title_tags = soup.find_all('span', class_='title')
    for title_tag in title_tags:
        titles.append(title_tag.string)
    return titles

def extract_candidates_from_title(titles):
    """
    extract kp from title
    :param titles: list, including a series of titles
    :return: keyphrases: list, including all the candidate
    """
    candidates = []
    for title in titles:
        cand = extract_candidate_chunks(title)
        candidates.extend(cand)
    return candidates



def extract_candidate_chunks(text):
    """
    extract candidate chunks from given text
    :param text: string: a single text
    :return: candidates: list, contain a series of candidate chunks
    """
    import nltk, itertools, string

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))

    # tokenize, POS-tag, and chunk using regular expressions
    grammar = "KT: {<JJ>* <NN.*>+}"
    chunker = nltk.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent)
                                      for sent in nltk.sent_tokenize(text))

    # ==== method 1======
    candidates_with_POS = []
    candidates = []
    tree_chunked_sents = [chunker.parse(tagged_sent) for tagged_sent in tagged_sents]
    for tree in tree_chunked_sents:
        for subtree in tree.subtrees():
            if subtree.label() == 'KT':
                candidates_with_POS.append(subtree.leaves())
    for cand in candidates_with_POS:
        NP = []
        for word, pos in cand:
            NP.append(word.lower())
        candidates.append(" ".join(NP))

    candidates = [candidate for candidate in candidates
                  if candidate not in stop_words
                  and not all(char in punct for char in candidate)]
    return candidates

# demo
# url = "http://dblp.uni-trier.de/pers/hd/f/F=uuml=rnkranz:Johannes"
# #
# titles = parser_title(url)
# candidates = extract_candidates_from_title(titles)
# for i, cand in enumerate(candidates):
#     print('i = ', i, "   ", cand)


# ========================================= part 2 ===========================================================

# meaningless!!!!!

# def parser_abstract(url):
#     """
#     parser title and abstract through google scholar
#     :param url: A DBLP url
#     :return: titles_abstracts: a dictionary {title: abstract}
#     """
#     from urllib.request import Request, urlopen
#     from bs4 import BeautifulSoup
#     import  urllib.error
#     import re
#     scholar_str = "http://scholar.google.com/"
#     scholar_urls = []
#     titles_abstracts = dict()
#     try:
#         req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
#     except urllib.error.HTTPError as e:
#         # Return code error (e.g. 404, 501, ...)
#         print('HTTPError: ' + str(e.code))
#     except urllib.error.URLError as e:
#         # Not an HTTP-specific error (e.g. connection refused)
#         # ...
#         print('URLError: ' + str(e.reason))
#     response = urlopen(req)
#     content = response.read()
#     soup = BeautifulSoup(content, 'html.parser')
#
#     navi_tags = soup.find_all('nav', class_='publ')
#     for navi_tag in navi_tags:
#         for tag in navi_tag.descendants:
#             if tag.name == 'a' and tag['href'].startswith(scholar_str):
#                 scholar_urls.append(tag['href'])
#     return scholar_urls
#
#
# url = "http://dblp.uni-trier.de/pers/hd/f/F=uuml=rnkranz:Johannes"
# scholar_urls = parser_abstract(url)
# for i, url in enumerate(scholar_urls):
#     print("i = ", i, "  ", url)