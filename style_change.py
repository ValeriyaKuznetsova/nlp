def change_style(text):
    lines = text.split("\n")
    words = [line.split(" ") for line in lines]
    for index_line, line in enumerate(words):
        for index, word in enumerate(line):
            if not word.islower():
                new_word = ""
                for index_letter, letter in enumerate(word):
                    if letter.isupper() and index_letter == 0 or letter.isdigit() and index_letter == 0:
                        new_word += letter.lower()
                    elif letter.isupper() or letter.isdigit():
                        new_word += "_"+letter.lower()
                    else:
                        new_word += letter
                line[index] = new_word
        words[index_line] = line
    return words



code = """MyVar17 = OtherVar
TheAnswer = 42"""
print(change_style(code))