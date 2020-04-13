def check_mail(address):
    addresses = ['gmail.com', 'mail.ru', 'yandex.com', 'edu.hse.ru']
    if '@' in address:
        address_parts = address.split('@')
        if address_parts[1] in addresses:
            return "Correct", address_parts[1]
    else:
        return "Your address is incorrect"


address = input()
print(check_mail(address))