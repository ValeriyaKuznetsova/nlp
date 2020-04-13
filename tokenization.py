import re


def tokenize(text: str) -> list:
    text += " "
    new_text = re.split('\W? ', text)[:-1]
    return new_text


text_new = """Меня зовут Лера. А как тебя зовут?"""
print(tokenize(text_new))