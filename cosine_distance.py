from collections import Counter
import math
from nltk import word_tokenize


def cos_similarity(counts_dict1, counts_dict2):
    unique = set(list(counts_dict1.keys()) + list(counts_dict2.keys()))
    numerator = 0
    denominator_1 = math.sqrt(sum([element**2 for element in counts_dict1.values()]))
    denominator_2 = math.sqrt(sum([element**2 for element in counts_dict2.values()]))
    denominator = denominator_1 * denominator_2
    for index, unique_element in enumerate(unique):
        numerator += counts_dict1[unique_element] * counts_dict2[unique_element]
    return numerator / denominator


def create_bag_of_words(sentence):
    words = [word.lower() for word in word_tokenize(sentence) if word.isalnum()]
    return Counter(words)


print(create_bag_of_words('I like swimming, and swimming'))
print(cos_similarity(Counter((1, 0, 0)), Counter((1, 6, 1))) == 0.3999999999999999)
print(cos_similarity(Counter((0, 1, 2)), Counter((1, 6, 1))) == 0.5163977794943222)
print(cos_similarity(Counter((1, 0, 0)), Counter((0, 1, 2))) == 0.7745966692414834)
print()
bag_of_words_1 = create_bag_of_words("The cat is on the mat.")
bag_of_words_2 = create_bag_of_words("The cat is on the chair.")
bag_of_words_3 = create_bag_of_words("I bought a new chair.")
print(cos_similarity(bag_of_words_1, bag_of_words_2) == 0.8749999999999998)
print(cos_similarity(bag_of_words_1, bag_of_words_3) == 0.0)
print(cos_similarity(bag_of_words_2, bag_of_words_3) == 0.15811388300841897)

