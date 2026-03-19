import sys
from core.rsa import RSA
from core.cipher import cipher

# Это для теста
# Генерирует ключ, печатает публичную часть степень и модуль соответственно
# Далее вводиться текст, ввод прекращается с Ctrl + D
# Выводиться шифро текст

key = RSA(16)
cip = cipher(key)
print(key.public_key)
encrypted_text = cip.encrypt(sys.stdin.read())
print(encrypted_text)

