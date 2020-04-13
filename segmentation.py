def split_sentences(text):
    if not text:
        return []
    punctuation = (".", "?", "!", "...")
    if text[-1] not in punctuation:
        text += "."
    text = text.replace('\n', " ")
    while "  " in text:
        text = text.replace("  ", " ")
    sentences = []
    sentence = ""
    for index in range(len(text)-2):
        if text[index] in punctuation and text[index-3:index+1] == "т.е.":
            sentence += text[index]
        elif text[index] in punctuation and text[index-2] in punctuation and text[index-3] == " ":
            sentence += text[index]
        elif text[index] in punctuation and text[index-2] in punctuation and text[index-3].isupper():
            sentence += text[index]
        elif text[index] in punctuation and text[index-3] in punctuation and text[index-2] == " " and text[index-4].isupper():
            sentence += text[index]
        elif text[index] in punctuation and text[index+2].isupper():
            sentences += [sentence + text[index]]
            sentence = ''
        elif text[index] in punctuation and text[index+1] == '"':
            sentences += [sentence + text[index]]
            sentence = ''
        elif text[index] in punctuation and text[index+2] == '"':
            sentences += [sentence + text[index]]
            sentence = ''
        else:
            sentence += text[index]
    return sentences


text = """Мама мыла раму. Мама мыла раму... Мама мыла раму? Мама мыла раму!
"Мама мыла раму?" "Нет, не мыла!" "А зря". Мама мыла т.н. раму. Мама мыла... раму.
Мама мыла раму для сестры, т.е. Нюры. Мама мыла раму для... Нюры.
Мама мыла раму, поговорив с И.А. Крыловым. Мама мыла раму, поговорив с И. А. Крыловым.
А.Б.В. Иванов. Мама мыла раму, поговорив с И. Крыловым.
"И.А. Крылов расскажет басни". "И. Крылов расскажет басни".
«Правда?» НЕКОТОРЫЕ ЛЮБЯТ КРИЧАТЬ. Т.к. Мила мыла раму, рама теперь чистая.
Какое-то время назад. 1. Первое предложение. 2. Второе предложение.
1812 год был трудным для России. Это предложение не оканчивается точкой
"""
print(split_sentences(text))


# ['Мама мыла раму', ' Мама мыла раму..', ' Мама мыла раму', ' Мама мыла раму!,
# "Мама мыла раму?" "Нет, не мыла!" "А зря"', ' Мама мыла т.н. раму', ' Мама мыла... раму',
# ' Мама мыла раму для сестры, т.е', ' Нюры', ' Мама мыла раму для..', ' Нюры',
# ' Мама мыла раму, поговорив с И.А', ' Крыловым', ' Мама мыла раму, поговорив с И',
# ' А', ' Крыловым', ' А.Б.В', ' Иванов', ' Мама мыла раму, поговорив с И', ' Крыловым. "И.А',
# ' Крылов расскажет басни". "И', ' Крылов расскажет басни". «Правда?» НЕКОТОРЫЕ ЛЮБЯТ КРИЧАТЬ',
# ' Т.к', ' Мила мыла раму, рама теперь чистая', ' Какое-то время назад. 1',
# ' Первое предложение. 2', ' Второе предложение. 1812 год был трудным для России']
