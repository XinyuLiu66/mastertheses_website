

# =============extract candidate chunks=================
def extract_candidate_chunks(text):

    import nltk, itertools, string

    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))

    # tokenize, POS-tag, and chunk using regular expressions
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

    # ==== method 2======
    # BOI_tagged_chunked_sents = [nltk.tree2conlltags(tree_chunked_sent)
    #                             for tree_chunked_sent in tree_chunked_sents]
    # all_chunks = list(itertools.chain.from_iterable(BOI_tagged_chunked_sents))
    #
    # #   get all the NP Chunk and exclude all the non-NP chunk
    # groups = []
    # for key, group in itertools.groupby(all_chunks, lambda x : x[2]!='O'):
    #     if(key):
    #         groups.append(list(group))
    #
    # # get all the candidate except stopwords and punkt
    # candidates = [" ".join(word for word, pos, chunk in group).lower()
    #               for group in groups]
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




# get all the titles, abstracts, keywords
def get_titles_abstracts_keywords(t_dic):
    # get all the abstracts
    abstracts = []
    titles = []
    keywords = []
    for text in t_dic:
        title = text['title']
        abs = text['abstract']
        keyword = text['keywords']
        titles.append(title)
        abstracts.append(abs)
        keywords.extend(keyword)
    return titles, abstracts, keywords