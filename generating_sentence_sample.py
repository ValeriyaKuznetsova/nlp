import re
import random
import math


def tokenize_sentence(text: str) -> list:
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


def get_log_probability(phrase: str, ngrams: dict, n, corp_size: int) -> int:
    log_prob = 0
    if len(tokenize_any_phrase(phrase)) == 1:
        return ngrams[phrase] / corp_size
    elif len(tokenize_sentence(phrase)) > n:
        tokens = tokenize_any_phrase(phrase)
        for word_index in range(len(tokens)-1, 0, -1):
            new_text = " ".join(tokens[word_index-n+1:word_index+1])
            prob_part = get_log_probability(new_text, ngrams, n, corp_size)
            log_prob += prob_part
    else:
        our_ngram = " ".join(tokenize_any_phrase(phrase))
        if our_ngram in ngrams:
            numerator = ngrams[our_ngram]
            part_of_text = " ".join(tokenize_any_phrase(phrase)[:-1])
            denominator = 0
            for ngram in ngrams:
                if part_of_text+" " in ngram:
                    denominator += ngrams[ngram]
            log_prob = math.log(numerator / denominator)
        else:
            log_prob = 0.0
    return log_prob


def get_log_probabilities(ngrams: dict, corpus: list) -> dict:
    log_probabilities = {}
    for ngram in ngrams:
        n = len(tokenize_any_phrase(ngram))
        corp_size = len(corpus)
        probability = get_log_probability(ngram, ngrams, n, corp_size)
        log_probabilities[ngram] = probability
    return log_probabilities


def generate_sentence_sample(prefix: str, corpus: str) -> str:
    """
    Chooses an appropriate ngram using the sample (if the length of the prefix > 1).
    Otherwise, doesn't do anything.
    :param prefix: a string which is going to be continued
    :param corpus: a text which will be the basis for generation
    :return: a generated sentence
    """
    sentence = prefix
    prefix = tokenize_any_phrase(prefix)
    n = len(prefix)
    tokens = tokenize_sentence(corpus)
    ngrams = get_ngram_counts(tokens, n)
    probabilities = get_log_probabilities(ngrams, tokens)
    ngram_variants = {}
    sum_probabilities = 0
    k = 0
    if n > 1:
        if n == 2:
            new_prefix = prefix[-1]
        else:
            new_prefix = " ".join(prefix[-n+1:])
        while sentence[-1] != "&":
            k += 1
            sum_probabilities_words = 0
            for ngram in probabilities:
                if new_prefix + " " in ngram:
                    ngram_variant = tokenize_any_phrase(ngram)[-n + 1]
                    ngram_variants[ngram_variant] = abs(probabilities[ngram])
                    sum_probabilities += abs(probabilities[ngram])
                elif new_prefix == "&":
                    break
            print("Варианты ngram: ", ngram_variants)
            print("Начальная сумма вероятностей: ", sum_probabilities)
            probability_for_sample = random.uniform(sum_probabilities, 0)
            print("Случайно выбранная вероятность: ", probability_for_sample)
            for ngram_variant, variant_probability in ngram_variants.items():
                print("Сравниваем вероятность ngram: ", ngram_variant, variant_probability + sum_probabilities_words)
                if variant_probability + sum_probabilities_words >= probability_for_sample:
                    print("ПОДХОДИТ!")
                    new_prefix = ngram_variant
                    break
                else:
                    sum_probabilities_words += variant_probability
                    print("Новая сумма вероятностей: ", sum_probabilities_words)
            sentence += " " + new_prefix
            print("Новое предложение: ", sentence, "\n")
            sum_probabilities = 0
            ngram_variants = {}
            if sentence[-1] == "&":
                sentence = sentence[:-2] + "."
                break
            if k == 50:
                break
    else:
        return "Are you sure that you want to do that with the sample method?"
    return sentence


#1 Sample generation
corpus = 'A dog and a cat were happy. I saw a cat and a dog. The cat was sleeping, and the dog was awake. ' \
         'I woke up the cat. I like a fish and a purple hat.'
print("Конечное предложение: ", generate_sentence_sample("dog was", corpus))


# 2 Sample with the Brown corpus
# with open("BROWN.txt", encoding='utf-8') as f:
#     corpus = f.read()
# print("Конечное предложение: ", generate_sentence_sample("the car", corpus))
