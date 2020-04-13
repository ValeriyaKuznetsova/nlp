import re


def tokenize(text: str) -> list:
    text += " "
    new_text = re.split('\W? ', text)[:-1]
    token_vowels = []
    for token in new_text:
        if re.match('[аеиоуыэяАЕИОУЫЭЯ]+.*', token):
            token_vowels += [token]
    return token_vowels


text_new = """Меня зовут Лера. А как тебя зовут? Я Екатерина. Люблю его"""
print(tokenize(text_new))