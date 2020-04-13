import nltk

brown_tagged = [('*', "START")]
brown_tagged += list(nltk.corpus.brown.tagged_words(categories="news", tagset='universal'))
brown_tagged_with_start = []
for (word, brown_tag) in brown_tagged:
    brown_tagged_with_start += [(word.lower(), brown_tag)]
    if (word, brown_tag) == ('.', '.'):
        brown_tagged_with_start += [('*', "START")]
brown_tagged_with_start.pop()
nltk_tag_frequencies = nltk.FreqDist(tag for (word, tag) in brown_tagged_with_start)
tag_frequencies = {tag: frequency for tag, frequency in nltk_tag_frequencies.items()}
word_tag_pairs = list(nltk.bigrams(brown_tagged_with_start))
tag_bigrams = [(bigram_1[1], bigram_2[1]) for (bigram_1, bigram_2) in word_tag_pairs]
tag_bigrams_frequencies = {}
for tag_bigram in tag_bigrams[:1000]:
    tag_frequency = tag_bigrams.count(tag_bigram)
    if tag_bigram not in tag_frequencies:
        tag_bigrams_frequencies[tag_bigram] = tag_frequency
print(brown_tagged_with_start[:100])

def find_emission_probability(tag: str, word: str) -> int:
    word_tag = (word, tag)
    word_tag_frequency = brown_tagged_with_start.count(word_tag)
    tag_frequency = tag_frequencies[tag]
    emission_probability = word_tag_frequency / tag_frequency
    return emission_probability


def find_transition_probability(tag_1: str, tag_2: str) -> int:
    tag_pair = (tag_1, tag_2)
    tag_pair_frequency = tag_bigrams_frequencies[tag_pair]
    all_pairs_first_tag_frequency = 0
    for tag_bigram in tag_bigrams_frequencies:
        if tag_1 in tag_bigram:
            all_pairs_first_tag_frequency += tag_bigrams_frequencies[tag_bigram]
    transition_probability = tag_pair_frequency / all_pairs_first_tag_frequency
    return transition_probability


def get_viterbi(sentence: str, states: list, trans_probabilities: dict, emis_probabilities: dict) -> list:
    viterbi = [[("START", 1.0)]]
    backpointers = []
    previous_probabilities = [("START", 1.0)]
    tokens = ["START"]
    tokens += nltk.word_tokenize(sentence.lower())
    for index_token, token in enumerate(tokens[1:]):
        viterbi.append([])
        probabilities = []
        probability_labels = []
        for state in states[1:]:
            for index_previous_state, (previous_state, previous_probability) in enumerate(previous_probabilities):
                trans_probability = 0.0
                emis_probability = 0.0
                if (previous_state, state) in trans_probabilities:
                    trans_probability = trans_probabilities[(previous_state, state)]
                if (state, token) in emis_probabilities:
                    emis_probability = emis_probabilities[(state, token)]
                probability_labels += [(previous_state, index_token)]
                probabilities += [previous_probability * trans_probability * emis_probability]
        max_probability = max(probabilities)
        max_probability_index = probabilities.index(max_probability)
        backpointers += [[probability_labels[max_probability_index], (states[max_probability_index+1], index_token+1)]]
        viterbi[-1] += [(states[max_probability_index+1], max_probability)]
        previous_probabilities = viterbi[-1]
    res_states = backpointers[-1][::-1]
    first_part = backpointers[-1][0]
    for backpointer in backpointers[::-1]:
        if first_part == backpointer[1]:
            res_states += [backpointer[0]]
            first_part = backpointer[0]
    res_states = res_states[::-1]
    for index, (res_state, index_token) in enumerate(res_states):
        for token in viterbi[index_token]:
            if res_state in token:
                probability_token = token[1]
                res_states[index] = (res_state, probability_token)
    return res_states


def make_whole_process(brown_sentence: list):
    tokens = [word for (word, tag) in brown_sentence]
    sentence_str = " ".join(tokens[1:])
    print(sentence_str)
    states = ["START", "ADV", "ADP", "ADJ", "DET", "NOUN", "VERB", ".", "PRT", "CONJ", "PRON", "NUM"]
    transition_probabilities = {("START", state): 1.0 for state in states}
    for (tag_1, tag_2) in tag_bigrams_frequencies:
        transition_probabilities[(tag_1, tag_2)] = find_transition_probability(tag_1, tag_2)

    emission_probabilities = {('START', 'START'): 1.0,
                              ('START', '.'): 0.0}
    for state in states:
        for token in tokens:
            emission_probabilities[(state, token)] = find_emission_probability(state, token)
    tags_probabilities = get_viterbi(sentence_str, states, transition_probabilities, emission_probabilities)
    return tags_probabilities


def evaluate(true_tags: list, tags_probabilities: list):
    mistakes = 0
    for index, (tag, probability) in enumerate(tags_probabilities):
        if index < len(true_tags):
            if tag != true_tags[index][1]:
                mistakes += 1
                print(tag, true_tags[index][1])
    return (len(tags_probabilities) - mistakes) / len(tags_probabilities)

# sentence = "The driver told police."
# sentence = "He is a student."
# sentence = "The Fulton County Grand Jury said Friday an investigation of recent primary election produced" \
#            "' no evidence ' that any irregularities took place."
# tokens = nltk.word_tokenize(sentence.lower())


end_first_sentence = brown_tagged_with_start.index(('.', '.'))
end_second_sentence =  brown_tagged_with_start[end_first_sentence+1:].index(('.', '.')) + end_first_sentence + 1
end_third_sentence = brown_tagged_with_start[end_second_sentence+2:].index(('.', '.')) + end_second_sentence + 2
first_sentence = brown_tagged_with_start[:end_first_sentence+1]
second_sentence = brown_tagged_with_start[end_first_sentence+1:end_second_sentence+1]
third_sentence = brown_tagged_with_start[end_second_sentence+1:end_third_sentence+1]
viterbi_second_sentence = make_whole_process(second_sentence)
print(viterbi_second_sentence)
print(evaluate(second_sentence, viterbi_second_sentence))
viterbi_third_sentence = make_whole_process(third_sentence)
print(evaluate(third_sentence, viterbi_third_sentence))

