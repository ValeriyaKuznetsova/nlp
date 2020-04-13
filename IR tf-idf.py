from nltk import word_tokenize
from pymystem3 import Mystem
import math
m = Mystem()

CORPUS = []
UNIQUE_WORDS_IN_CORPUS = []
for i in range(1, 102):
    # name_of_file = "задание_6_news/({}).txt".format(str(i))
    name_of_file = "задание_6_news_lem/_lem({}).txt".format(str(i))
    with open(name_of_file, "r") as f:
        text = f.read().replace("\n", " ")
        CORPUS += [text.lower()]
        UNIQUE_WORDS_IN_CORPUS += set([word.lower() for word in word_tokenize(text) if word.isalpha()])


def all_df(corpus: list, unique_words_in_corpus: list):
    inverted_index = {}
    for word in unique_words_in_corpus:
        inverted_index[word] = []
        for index, text in enumerate(corpus):
            if word in text:
                inverted_index[word].append(index+1)
    return inverted_index


def all_idf(corpus: list, inverted_index: dict):
    n = len(corpus)
    inverted_frequencies = {}
    for word in inverted_index:
        inverted_frequencies[word] = math.log(n / len(inverted_index[word]))
    return inverted_frequencies


def all_tf(term: str, corpus: list):
    term_frequencies = []
    for text in corpus:
        frequency = text.count(term)
        if not frequency:
            term_frequencies += [0]
            continue
        term_frequencies += [1 + math.log(frequency)]
    return term_frequencies


def find_tf_idf(term: str, corpus: list):
    tf_idf = []
    inverted_index = all_df(corpus, UNIQUE_WORDS_IN_CORPUS)
    term_frequencies = all_tf(term, corpus)
    inverted_frequencies = all_idf(corpus, inverted_index)
    for index in range(len(corpus)):
        term_frequency = term_frequencies[index]
        term_inverted_frequency = inverted_frequencies[term]
        tf_idf += [term_frequency * term_inverted_frequency]
    return tf_idf


query = input("Write your query: ").split()
sum_tf_idf = []
for index_word, word in enumerate(query):
    inverted_index = all_df(CORPUS, UNIQUE_WORDS_IN_CORPUS)
    inverted_frequencies = all_idf(CORPUS, inverted_index)
    term_frequencies = all_tf(word, CORPUS)
    all_tf_idf = find_tf_idf(word, CORPUS)
    for index in range(len(all_tf_idf)):
        if index_word == 0:
            sum_tf_idf += [all_tf_idf[index]]
        else:
            sum_tf_idf[index] += all_tf_idf[index]
relevant_documents = {}
for index, tf_idf in enumerate(sum_tf_idf):
    if tf_idf != 0:
        relevant_documents[index] = tf_idf
print(sorted(relevant_documents.keys(), key=relevant_documents.__getitem__, reverse=True))