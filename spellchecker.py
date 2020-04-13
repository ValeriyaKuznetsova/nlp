import re


def get_words(text: str) -> list:
    text += " "
    text = text.replace('\n', " ")
    tokens = re.split('\W? ', text)[:-1]
    return tokens


def get_counts(tokens: list) -> dict:
    frequencies = {}
    for token in tokens:
        if token not in frequencies:
            frequencies[token] = tokens.count(token)
    return frequencies


def get_edits1(word: str) -> list:
    word_variants = [word]
    for letter in range(1072, 1103):
        # add one letter
        for place in range(len(word)+1):
            new_word = word[:place] + str(chr(letter)) + word[place:]
            if new_word not in word_variants:
                word_variants.append(new_word)
        # change one letter
        for place in range(len(word)):
            new_word = word[:place] + str(chr(letter)) + word[place+1:]
            if new_word not in word_variants:
                word_variants.append(new_word)
    # delete one letter
    for place in range(len(word)):
        new_word = word[:place] + word[place+1:]
        if new_word not in word_variants:
            word_variants.append(new_word)
    # mix adjacent letters
    for place in range(1, len(word)):
        left = word[:place-1] + word[place]
        right = word[place-1] + word[place+1:]
        new_word = left + right
        if new_word not in word_variants:
            word_variants.append(new_word)
    return word_variants


def get_most_likely(word: str, frequencies: dict) -> str:
    if word in frequencies:
        return word
    else:
        word_variants = get_edits1(word)
        answer = word[::]
        max_frequency = 0
        for variant in word_variants:
            if variant in frequencies and frequencies[variant] > max_frequency:
                answer = variant
                max_frequency = frequencies[variant]
        return answer


# tokens = get_words("Я люблю мороженое")
# frequencies = get_counts(tokens)
# print(get_most_likely('мороженное', frequencies))

with open("lifenews.txt") as f:
    text = f.read().lower()
    tokens = get_words(text)
    frequencies = get_counts(tokens)
    print(get_most_likely("покудатели", frequencies))
