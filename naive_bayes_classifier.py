
def get_features(word_list_name: str):
    with open(word_list_name, encoding='utf-8') as f:
        words = f.read().split("\n")
    return words


def extract_features(text, features):
    """
    "Превращает" текст в вектор (список) признаков, т.е. чисел.
    Каждая позиция в списке - количество вхождений соответствующего слова из списка features в тексте text.
    Вход: text (строка), features (список слов)
    Выход: список целых чисел
    """
    text_vector = []
    for feature in features:
        text_vector.append(text.count(feature))
    return text_vector


def train_nbc(features, corpora):
    """
    Эта функция собственно "обучает" классификатор на корпусах.
    Необходимо посчитать параметры для двух моделей: модель положительных отзывов и модель отрицательных отзывов,
    на двух соответствующих корпусах. Другими словами, в одном списке должно быть два вложенных списка параметров,
    каждый длиной n, где n - количество признаков (слов). Каждый параметр считается так:
    количество вхождений соответствующего признака (слова) в соответствующем корпусе
    (положительном, когда строим первую модель, и отрицательном, когда строим вторую),
    делённое на суммарное количество вхождений всех признаков в данном корпусе.
    :param features:
    :param corpora:
    :return:
    """
    models = []
    for index, corpus in enumerate(corpora):
        text_vector = extract_features(corpus, features)
        text_vector_with_parameters = [(feature+1)/(sum(text_vector)+len(features)) for feature in text_vector]
        models += [text_vector_with_parameters]
    return models


def classify(text, features, classes, priors, params):
    """
    Для каждого класса считает произведение вероятностей: вероятность класса
    (или prior) * вероятность каждого слова-признака для данного класса, возведённая в степень k,
    где k - абсолютная частота данного слова В АНАЛИЗИРУЕМОМ ТЕКСТЕ (а не в корпусе). :
    """
    class_probabilities = [1, 1]
    for index in range(len(classes)):
        class_probabilities[index] *= priors[index]
        for index_feature, probability in enumerate(params[index]):
            k = text.count(features[index_feature])
            class_probabilities[index] *= probability ** k
    if class_probabilities[0] > class_probabilities[1]:
        return classes[0]
    return classes[1]


def evaluate(hypotheses, true_answers, klass='all'):
    classes = ['pos', 'neg']
    metrics = []
    for one_class in classes:
        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0
        for index in range(len(hypotheses)):
            if hypotheses[index] == true_answers[index]:
                if hypotheses[index] == one_class:
                    true_positives += 1
                else:
                    true_negatives += 1
            else:
                if hypotheses[index] == one_class:
                    false_positives += 1
                else:
                    false_negatives += 1
        accuracy = (true_positives + true_negatives) / len(hypotheses)
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1 = 2 * precision * recall / (precision + recall)
        metrics += [[accuracy, precision, recall, f1]]
    print(metrics)
    accuracy_mean = (metrics[0][0] + metrics[1][0]) / 2
    precision_mean = (metrics[0][1] + metrics[1][1]) / 2
    recall_mean = (metrics[0][2] + metrics[1][2]) / 2
    f1_mean = (metrics[0][3] + metrics[1][3]) / 2
    return (accuracy_mean, precision_mean, recall_mean, f1_mean)


with open('test_text.txt', encoding='utf-8') as f:
    text = f.read()
features = get_features('vocab_films.txt')
text_vector = extract_features(text, features)
corpus_pos = open('pos_train.txt', encoding='utf-8').read()
corpus_neg = open('neg_train.txt', encoding='utf-8').read()
corpora = corpus_pos, corpus_neg
classes = 'positive', 'negative'
params = train_nbc(features, corpora)
priors = 0.5, 0.5
text1 = 'The movie was horrible, it was absolutely awful.'
label1 = classify(text1, features, classes, priors, params)
text2 = 'I really enjoyed the film, it was fantastic.'
label2 = classify(text2, features, classes, priors, params)
# print(label1, label2)  # ожидаемый вывод программы: negative positive

h = ('pos', 'neg', 'pos', 'pos', 'neg', 'pos', 'neg', 'pos', 'neg', 'pos')
y = ('pos', 'neg', 'pos', 'neg', 'neg', 'neg', 'neg', 'neg', 'pos', 'neg')
print(evaluate(h, y))




