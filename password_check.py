def check_password(password):
    check_digit = False
    check_upper_case = False
    check_lower_case = False
    check_symbols = False
    if len(password) < 10:
        return "Incorrect"
    for letter in password:
        if letter.isdigit():
            check_digit = True
            check_symbols = True
        elif letter.isupper():
            check_upper_case = True
            check_symbols = True
        elif letter.islower():
            check_lower_case = True
            check_symbols = True
        elif letter == "_":
            check_symbols = True
        else:
            return "Incorrect"
    if check_symbols and check_lower_case and check_upper_case and check_digit:
        return "Correct"
    else:
        return "Incorrect"


password = input()
print(check_password(password))