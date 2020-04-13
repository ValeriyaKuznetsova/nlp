import pymystem3

text = """Мой дядя самых честных правил,
Когда не в шутку занемог,
Он уважать себя заставил
И лучше выдумать не мог.
"""

m = pymystem3.Mystem()
lemmas = m.lemmatize(text)
print(''.join(lemmas))

analysis = m.analyze(text)
nouns_case = []
for word_analysis in analysis:
    noun_case = ""
    if 'analysis' in word_analysis:
        grammar = word_analysis['analysis'][0]['gr']
        if grammar[:2] == "S,":
            noun_case += word_analysis['text'] + " "
            noun_case += grammar[grammar.index("=")+1:grammar.rfind(',')]
            nouns_case += [noun_case]
print(nouns_case)