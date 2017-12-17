# ================score key phrases by textrank=================
import sys
sys.path.append('../..')
from mastertheses.set_person_profile.extract_candidates.extract_candidate_chunks_and_words import *

# n_keywords: number of keywords in a window. That is, n_keywords * len(words)
def score_keyphrases_by_textrank(text, title, n_keywords=0.1):
    from itertools import takewhile, tee
    import networkx, nltk

    # tokenize for all words, and extract *candidate* words
    words = [word.lower() for sent in nltk.sent_tokenize(text)
                            for word in nltk.word_tokenize(sent)]
    candidates = extract_candidate_words(text)

    # build graph, each node is a unique candidate
    graph = networkx.Graph()
    graph.add_nodes_from(set(candidates))

    # iterate over word-pairs, add unweighted edges into graph
    # TODO !!!!!!  need to be weighted, also using keywords and title as reference
    # get bigram phrase from the word an it's neighborhood
    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a,b = tee(iterable, 2)
        next(b)
        return zip(a,b)

    for w1, w2 in pairwise(candidates):
        if w2:
            graph.add_edge(*sorted([w1, w2]))   # * mean divide list to 2 independent element

    # score nodes using default pagerank algorithm, sort by score, keep top n_keywords
    ranks = networkx.pagerank(graph)
    if 0 < n_keywords <1:
        n_keywords = int(round(len(candidates) * n_keywords))

    word_ranks = {word_rank[0]: word_rank[1]
                  for word_rank in sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:n_keywords]}
    # test
    # print("ranks :", ranks)

    keywords = set(word_ranks.keys())
    # merge keywords into keyphrases
    keyphrases = {}
    j = 0
    for i, word in enumerate(words):
        if i < j:
            continue
        if word in keywords:
            kp_words = list(takewhile(lambda x: x in keywords, words[i:i+10]))
            avg_pagerank = sum(word_ranks[w] for w in kp_words)/float(len(kp_words))
            keyphrases[" ".join(kp_words)] = avg_pagerank
            # counter as hackish way to ensure merged keyphrases are non-overlapping
            j = i + len(kp_words)

    sorted_chunks = sorted(keyphrases.items(), key=lambda x: x[1], reverse=True)
    sorted_chunks = score_again_to_candidate(sorted_chunks, title)
    return sorted_chunks



def score_again_to_candidate(all_chunks, titles):
    BIAS_TO_WORD_IN_TITLE = 2
    if titles:
        for i, chunk in enumerate(all_chunks):
            if set(chunk[0].split(" ")).intersection(set(titles)):
                chunk = list(chunk)
                chunk[1] *= BIAS_TO_WORD_IN_TITLE
                chunk = tuple(chunk)
                all_chunks[i] = chunk
    else:
        pass
    return all_chunks



# score each candidate using titles and keywords information, give bias to each candidate
def get_titles_keywords_by_words(titles, keywords):
    titles_by_words = list()
    keywords_by_words = list()
    for phrase in titles:
        titles_by_words.extend(phrase.split())
    for keyword in keywords:
        keywords_by_words.extend(keyword.split())
    return titles_by_words, keywords_by_words