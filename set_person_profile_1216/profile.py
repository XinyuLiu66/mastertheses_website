#!/usr/bin/python

"""
TF * IDF method extract key phrases
"""

# ========================================mportant method (in main)==============================================
def parser_title(url):
    """
    parser all the titles from DBLP
    :param url: a dblp url
    :return: titles, a list of title
    """
    # from urllib.request import Request, urlopen
    import urllib
    from bs4 import BeautifulSoup
    titles = []   # results
    response = urllib.urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content, 'html.parser')
    title_tags = soup.find_all('span', class_='title')
    for title_tag in title_tags:
        titles.append(title_tag.string)
    return titles


# ====================================important method (in main)======================================================
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


# ======================== was called by extract_candidates_from_title =============================
def extract_candidate_chunks(text, typ='title'):
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
    if typ == 'title':
        grammar = "KT: {<JJ>* <NN.*>+}"
    else:
        grammar = "KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}"
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

# =============extract candidate keywords, formulate [ WordNet ]=================
def extract_candidate_words(text):
    import itertools, nltk, string
    good_tags = ['JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNS', 'NNPS']

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))

    # tokenize and POS-tag words
    sentences = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]
    tagged_sentences = nltk.pos_tag_sents(sentences)
    tagged_words = itertools.chain.from_iterable(tagged_sentences)

    # filter on certain POS tags and lowercase all words
    candidates = [word.lower() for word, tag in tagged_words
                  if(tag in good_tags) and word.lower() not in stop_words
                  and not all(char in punct for char in word)]

    return candidates

# =================================================================================================
def score_keyphrases_by_tfidf(texts, candidates='chunks'):
    """
    use tf*idf method to score key phrase
    :param texts: TODO list!!!!, a number of text
    :param candidates: could be chunks or words
    :return:
    """
    import gensim
    # extract candidates from each text in texts, either chunks or words
    if candidates == 'chunks':
        boc_texts = [extract_candidate_chunks(text) for text in texts]
    elif candidates == 'words':
        boc_texts = [extract_candidate_words(text) for text in texts]

    # make gensim dictionary and corpus
    dictionary = gensim.corpora.Dictionary(boc_texts)

    # Convert document (a list of words) into the bag-of-words format = list of (token_id, token_count) 2-tuples
    corpus = [dictionary.doc2bow(boc_text) for boc_text in boc_texts]
    # transform corpus with tf*idf model
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]  # corpus_tfidf: a list of 2-tuple (id, score)
    return corpus_tfidf, dictionary  # dictionary: {id: key phrase}









# =================================================================================================

def main(argv):
    import itertools
    url = argv[0]
    # url = "http://dblp.uni-trier.de/pers/hd/f/F=uuml=rnkranz:Johannes"
    sorted_chunk_score = []
    titles = parser_title(url)
    corpus_tfidf, dictionary = score_keyphrases_by_tfidf(titles)
    chunkID_scores = itertools.chain.from_iterable(corpus_tfidf)  # a list of tuple (chunk_ID, scores)
    # sorted according to scores from top to bottom
    chunkID_scores = list(chunkID_scores)
    chunkID_scores.sort(key=lambda x: x[1], reverse=True)
    for chunkID, score in chunkID_scores:
        sorted_chunk_score.append((dictionary.get(chunkID), score))

    print(sorted_chunk_score)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
