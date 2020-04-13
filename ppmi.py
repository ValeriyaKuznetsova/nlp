import math


counts = {'апельсин': {'вкусный': 1,
                       'данные': 0,
                       'компьютер': 0,
                       'результат': 0,
                       'сладкий': 1},
          'информация': {'вкусный': 0,
                         'данные': 6,
                         'компьютер': 1,
                         'результат': 4,
                         'сладкий': 0},
          'цифровой': {'вкусный': 0,
                       'данные': 1,
                       'компьютер': 2,
                       'результат': 1,
                       'сладкий': 0},
          'яблоко': {'вкусный': 1,
                     'данные': 0,
                     'компьютер': 1,
                     'результат': 0,
                     'сладкий': 1}}


def find_pmi(word_1, word_2, counts):
    all_count = sum([sum(row.values()) for row in counts.values()])
    numerator = counts[word_1][word_2] / all_count
    denominator_1 = sum(counts[word_1].values()) / all_count
    denominator_2 = sum([row[word_2] for row in counts.values() if word_2 in row]) / all_count
    denominator = denominator_1 * denominator_2
    pmi = math.log2(numerator / denominator)
    return pmi


def find_ppmi(word_1, word_2, counts):
    pmi = find_pmi(word_1, word_2, counts)
    if pmi < 0:
        return 0
    return pmi


def add_2_to_count(counts):
    for word_counts in counts.values():
        for each_word in word_counts:
            word_counts[each_word] += 2
    return counts


print(find_pmi("информация", "данные", counts))
print(find_pmi("информация", "данные", counts) == 0.6401040549136171)
print(find_pmi("информация", "результат", counts) == 0.5405683813627028)
print(find_ppmi("информация", "результат", counts) == 0.5405683813627028)
print(find_pmi("информация", "компьютер", counts) == -1.137503523749935)
print(find_ppmi("информация", "компьютер", counts) == 0)
print()
counts_2 = add_2_to_count(counts)
print(find_pmi("информация", "данные", counts_2))
print(find_pmi("информация", "результат", counts_2))
print(find_ppmi("информация", "результат", counts_2))
print(find_pmi("информация", "компьютер", counts_2))
print(find_ppmi("информация", "компьютер", counts_2))