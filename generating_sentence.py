import re
import random


def tokenize(text: str) -> list:
    if not text:
        return []
    ord_list = (33, 63, 46)
    if ord(text[-1]) not in ord_list:
        return []
    text = text.replace('\n', " ")
    while "  " in text:
        text = text.replace("  ", " ")
    words = text.split(" ")
    while "" in words:
        words.remove("")
    sentences = ["*"]
    ord_list = (33, 63, 46)
    for index, word in enumerate(words):
        if not word[-1].isalpha() and index == (len(words) - 1):
            sentences.append(word[:-1])
            sentences.append("&")
        elif ord(word[-1]) in ord_list and words[index + 1][0].isupper():
            sentences.append(word[:-1])
            sentences.append("&")
            sentences.append("*")
        else:
            sentences.append(word)
    new_sentences = []
    for index, word in enumerate(sentences):
        new_word = ""
        if not word.isalpha() and (not word == '*' and not word == "&"):
            for i in word:
                if i.isalpha():
                    new_word += i
            if new_word:
                new_sentences.append(new_word.lower())
        else:
            new_sentences.append(word.lower())
    if new_sentences[0] == ["*", "&"]:
        return []
    return new_sentences


def tokenize_any_phrase(phrase: str) -> list:
    tokenized_phrase = re.findall('\S+', phrase)
    return tokenized_phrase


def get_ngram_counts(tokens: list, n: int) -> dict:
    ngram_counts = {}
    for i in range(len(tokens) - 1):
        ngram = tokens[i:i + n]
        if " ".join(ngram) == "& *":
            continue
        if not " ".join(ngram).lower() in ngram_counts:
            ngram_counts[" ".join(ngram).lower()] = 1
        else:
            ngram_counts[" ".join(ngram).lower()] += 1
    return ngram_counts


def get_probability(text: str, ngrams: dict, n: int, corp_size: int) -> int:
    probability = 1.0
    if len(text) == 1:
        return ngrams[text] / corp_size
    elif len(tokenize(text)) > n:
        tokens = tokenize(text)
        for word_index in range(len(tokens)-1, 0, -1):
            ngram = " ".join(tokens[word_index-n+1:word_index+1])
            prob_part = get_probability(ngram, ngrams, n, corp_size)
            probability *= prob_part
    else:
        our_ngram = " ".join(tokenize(text))
        numerator = 1
        if our_ngram in ngrams:
            numerator += ngrams[our_ngram]
        part_of_text = " ".join(tokenize(text)[:-1])
        denominator = len(ngrams)
        for ngram in ngrams:
            if part_of_text+" " in ngram:
                denominator += ngrams[ngram]
        probability = numerator / denominator
    return probability


def generate_sentence_greedy(prefix: str, corpus: str) -> str:
    """
    Chooses an appropriate ngram with the highest probability.
    :param prefix: a string which is going to be continued
    :param corpus: a text which will be the basis for generation
    :return: a generated sentence
    """
    sentence = prefix
    prefix = tokenize_any_phrase(prefix)
    n = len(prefix)
    if n == 1:
        n += 1
    tokens = tokenize(corpus)
    print(tokens)
    ngrams = get_ngram_counts(tokens, n)
    max_probability = 0
    ngram_variant = ""
    if n <= 2:
        new_prefix = prefix[-1]
    else:
        new_prefix = " ".join(prefix[-n+1:])
    while sentence[-1] != "&":
        for ngram in ngrams:
            if new_prefix+" " in ngram and ngrams[ngram] > max_probability:
                ngram_variant = tokenize_any_phrase(ngram)[-n+1]
                max_probability = ngrams[ngram]
            elif new_prefix == "&":
                break
        if new_prefix == "":
            return "I DON'T KNOW"
        new_prefix = ngram_variant
        print("Ngram с максимальной вероятностью: ", new_prefix)
        sentence += " " + new_prefix
        print("Новое предложение: ", sentence)
        max_probability = 0
        if sentence[-1] == "&":
            sentence = sentence[:-2] + "."
            break
    return sentence


def generate_sentence_random(prefix: str, corpus: str) -> str:
    """
    Chooses a random appropriate ngram.
    :param prefix: a string which is going to be continued
    :param corpus: a text which will be the basis for generation
    :return: a generated sentence
    """
    sentence = prefix
    prefix = tokenize_any_phrase(prefix)
    n = len(prefix)
    if n == 1:
        n += 1
    tokens = tokenize(corpus)
    ngrams = get_ngram_counts(tokens, n)
    ngram_variants = []
    if n <= 2:
        new_prefix = prefix[-1]
    else:
        new_prefix = " ".join(prefix[-n+1:])
    while sentence[-1] != "&":
        for ngram in ngrams:
            if new_prefix+" " in ngram:
                ngram_variant = tokenize_any_phrase(ngram)[-n+1]
                ngram_variants += [ngram_variant]
            elif new_prefix == "&":
                break
        if not ngram_variants:
            return "I DON'T KNOW"
        print("Варианты ngram: ", ngram_variants)
        new_prefix = random.choice(ngram_variants)
        print("Случайно выбранная ngram: ", new_prefix)
        sentence += " " + new_prefix
        print("Новое предложение: ", sentence, "\n")
        ngram_variants = []
        if sentence[-1] == "&":
            sentence = sentence[:-2] + "."
            break
    return sentence


#1 Random generation
# corpus = 'A dog and a cat were happy. I saw a cat and a dog. The cat was sleeping, and the dog was awake. ' \
#          'I woke up the cat. I like a fish and a purple hat.'
# print('Конечное предложение: ', generate_sentence_random("a cat", corpus))

#2 Greedy generation
# corpus = 'A dog and a cat were happy. I saw a cat and a dog. The cat was sleeping, and the dog was awake. ' \
#          'I woke up the cat. I like a fish and a purple hat and a dog.'
# print('Конечное предложение: ', generate_sentence_greedy("a cat", corpus))


#3 Both with the Brown corpus
# with open("BROWN.txt", encoding='utf-8') as f:
#     corpus = f.read()
# print("Конечное предложение greedy: ", generate_sentence_greedy("the car", corpus), "\n\n")
# print("Конечное предложение random: ", generate_sentence_random("the car", corpus))
