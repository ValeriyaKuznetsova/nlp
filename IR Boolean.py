from nltk import word_tokenize
from pymystem3 import Mystem
m = Mystem()

corpus = []
unique_words_in_corpus = []
for i in range(1, 102):
    # name_of_file = "задание_6_news/({}).txt".format(str(i))
    name_of_file = "задание_6_news_lem/_lem({}).txt".format(str(i))
    with open(name_of_file, "r") as f:
        text = f.read().replace("\n", " ")
        corpus += [text.lower()]
        unique_words_in_corpus += set([word.lower() for word in word_tokenize(text) if word.isalpha()])


def all_df(corpus: list, unique_words_in_corpus: list):
    inverted_index = {}
    for word in unique_words_in_corpus:
        inverted_index[word] = []
        for index, text in enumerate(corpus):
            if word in text:
                inverted_index[word].append(index+1)
    return inverted_index


def boolean_search(inverted_index: dict):
    query = input("Write your query: ").split()
    # query = [m.lemmatize(word)[0] for word in input("Write your query: ").split()]
    relevant_documents = []
    documents_with_all_query_words = []
    for word in query:
        if word in inverted_index:
            relevant_documents += inverted_index[word]
            relevant_documents.sort()
    for index in range(len(relevant_documents)):
        if relevant_documents.count(relevant_documents[index]) >= len(query)\
                and relevant_documents[index] not in documents_with_all_query_words:
            documents_with_all_query_words += [relevant_documents[index]]
    return documents_with_all_query_words


def boolean_search_2(inverted_index: dict):
    # query = input("Write your query: ").split()
    query = [m.lemmatize(word)[0] for word in input("Write your query: ").split()]
    relevant_documents = []
    documents_with_all_query_words = ()
    for word in query:
        if word in inverted_index:
            relevant_documents += [inverted_index[word]]
            relevant_documents.sort()
    print(relevant_documents)
    if len(query) == 1:
        return relevant_documents[0]
    for index in range(len(relevant_documents)-1):
        documents_with_all_query_words = set.intersection(set(relevant_documents[index]),
                                                          set(relevant_documents[index+1]))
    return documents_with_all_query_words


inverted_index = all_df(corpus, unique_words_in_corpus)
print(boolean_search_2(inverted_index))

