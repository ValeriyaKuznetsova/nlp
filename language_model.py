import re


def tokenize(text: str) -> list:
    text += " "
    tokens = re.split('\W? ', text)[:-1]
    return tokens


def get_ngram_counts(words: list, n: int) -> dict:
    ngram_counts = {}
    start = ["<s> "] * (n - 1)
    finish = [" </s>"] * (n - 1)
    words = start + words + finish
    for i in range(len(words)-1):
        ngram = words[i:i+n]
        if not " ".join(ngram).lower() in ngram_counts:
            ngram_counts[" ".join(ngram).lower()] = 1
        else:
            ngram_counts[" ".join(ngram).lower()] += 1
    return ngram_counts


def get_prob(text: str, ngrams: dict, n, corp_size: int) -> int:
    prob = 1.0
    if len(text) == 1:
        return ngrams[text] / corp_size
    elif len(tokenize(text)) > n:
        tokens = tokenize(text)
        for word_index in range(len(tokens)-1, 0, -1):
            new_text = " ".join(tokens[word_index-n+1:word_index+1])
            prob_part = get_prob(new_text, ngrams, n, corp_size)
            prob *= prob_part
    else:
        our_ngram = " ".join(tokenize(text))
        if our_ngram in ngrams:
            numerator = ngrams[our_ngram]
            part_of_text = " ".join(tokenize(text)[:-1])
            denominator = 0
            for ngram in ngrams:
                if part_of_text+" " in ngram:
                    denominator += ngrams[ngram]
            prob = numerator / denominator
        else:
            prob = 0.0
    return prob


corpus = 'I saw a cat and a dog. The cat was sleeping, and the dog was awake. I woke up the cat.'
words = tokenize(corpus)
corp_size = len(words)
ngrams = get_ngram_counts(words, 2)
tests = ('a cat', 'the cat', 'the dog', 'the woke', 'the cat was awake')
for t in tests:
    print(t, get_prob(t, ngrams, 2, corp_size))
