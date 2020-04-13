import re

# добавила в trans_prob, emis_prob 0.0

def get_viterbi(sentence: str, states: list, trans_probabilities: dict, emis_probabilities: dict) -> list:
    viterbi = [[('[START]', 1.0)]]
    backpointers = []
    previous_probabilities = [('[START]', 1.0)]
    tokens = ['[START]']
    tokens += re.findall('\S+', sentence)
    tokens += ['[END]']
    for index_token, token in enumerate(tokens[1:]):
        viterbi.append([])
        for state in states[1:]:
            probabilities = []
            probability_labels = []
            for index_previous_state, (previous_state, previous_probability) in enumerate(previous_probabilities):
                trans_probability = trans_probabilities[(previous_state, state)]
                emis_probability = emis_probabilities[(state, token)]
                probability_labels += [(previous_state, index_token)]
                probabilities += [previous_probability * trans_probability * emis_probability]
            max_probability = max(probabilities)
            max_probability_index = probabilities.index(max_probability)
            backpointers += [[probability_labels[max_probability_index], (state, index_token+1)]]
            viterbi[-1] += [(state, max_probability)]
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


states = ['[START]', 'noun', 'verb', '[END]']

# transition probabilities
trans_probabilities = {('[START]', 'verb'): 0.2,
                       ('[START]', 'noun'): 0.8,
                       ('noun', 'verb'): 0.8,
                       ('noun', '[END]'): 0.1,
                       ('noun', 'noun'): 0.1,
                       ('verb', 'noun'): 0.2,
                       ('verb', 'verb'): 0.1,
                       ('verb', '[END]'): 0.7,
                       ('[START]', '[END]'): 0.0,
                       ('[END]', 'noun'): 0.0,
                       ('[END]', 'verb'): 0.0,
                       ('[END]', '[END]'): 0.0}

# emission probabilities
emis_probabilities = {('noun', 'fish'): 0.8,
                      ('noun', 'sleep'): 0.2,
                      ('verb', 'fish'): 0.5,
                      ('verb', 'sleep'): 0.5,
                      ('[END]', '[END]'): 1.0,
                      ('[START]', '[START]'): 1.0,
                      ('[START]', '[END]'): 0.0,
                      ('[END]', '[START]'): 0.0,
                      ('[END]', 'fish'): 0.0,
                      ('[END]', 'sleep'): 0.0,
                      ('noun', '[END]'): 0.0,
                      ('verb', '[END]'): 0.0}

sentence = 'sleep sleep sleep'
print(get_viterbi(sentence, states, trans_probabilities, emis_probabilities))
