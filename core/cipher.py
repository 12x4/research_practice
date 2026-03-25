import math
import random
import secrets
import logging

# from utils_for_rsa import *
# from rsa import RSA


class cipher:

    def __init__(self, rsa_key):
        self.key = rsa_key

    # Шифровка
    def encrypt(self, plaintext):

        encrypted_text = ""

        for char in plaintext.lower():
            encrypted_text += str(self.key.public_key.mod_pow(ord(char))) + " "

        return encrypted_text

    # Расшифровка
    def decrypt(self, ciphertext):
        decrypted_text = ""

        for char in ciphertext.split(" "):
            if char != "":
                decrypted_text += chr(self.key.private_key.mod_pow(int(char)))

        return decrypted_text


class cipher_2(cipher):

    def __init__(self, rsa_key):
        super().__init__(rsa_key)

    # Мега шифр
    # Шифрует с алгоритмом rsa блоками
    def encrypt_to_bytes(self, plaintext):

        mass_bytes = self.str_to_bytes(plaintext)
        r = self.from_bytes(mass_bytes)

        if self.key.public_key.module <= r:
            raise ValueError("Слишком маленький ключ для шифрования")

        y = self.key.public_key.mod_pow(r)

        print(r)
        print(y)

        mass_bytes_enc = self.to_bytes(y)
        enc_text = self.bytes_to_str(mass_bytes_enc)

        return enc_text

    # Превращает строку в байты
    def str_to_bytes(self, text: str) -> bytearray:

        list_bytes = []

        for char in text:

            if ord(char) > 255:
                logging.error("Обнаружен символ число которого больше 255")
                raise ValueError("Обнаружен символ число которого больше 255")

            list_bytes.append(ord(char))
        return bytearray(list_bytes)

    # Превращает байты в строку
    def bytes_to_str(self, mass_bytes: bytearray) -> str:
        text = ""

        for char in mass_bytes:

            try:
                text += chr(char)
            except Exception as e:
                logging.error("Ошибка при переходе bytearray в string")
                raise Exception("Ошибка при переходе bytearray в string")

        return text

    # Число в байты
    def to_bytes(self, num: int, byte_count=None, byteorder="big", abc=None) -> bytearray:

        result_bytearray = None
        byte_list = []

        if abc is None:

            if num == 0:
                byte_list.append(0)

            while num != 0:
                byte_list.append(num % 256)
                num //= 256

            if byte_count is not None and len(byte_list) < byte_count:
                for _ in range(byte_count - len(byte_list)):
                    byte_list.append(0)


        else:
            abc_len = len(abc)

            if num == 0:
                byte_list.append(ord(abc[0]))

            while num != 0:

                byte_list.append(ord(abc[num % abc_len]))
                num //= abc_len

            if byte_count is not None and len(byte_list) < byte_count:
                for _ in range(byte_count - len(byte_list)):
                    byte_list.append(ord(abc[0]))

        if byteorder == "big":
            result_bytearray = bytearray(byte_list[::-1])
        elif byteorder == "little":
            result_bytearray = bytearray(byte_list)
        else:
            logging.error("from_bytes вызван неправильным аргументом byteorder")
            raise TypeError

        return result_bytearray

    # Байты в число
    def from_bytes(self, mass_bytes: bytearray, byteorder="big") -> int:

        result_num = 0

        if byteorder == "big":
            mass_bytes = mass_bytes[::-1]
            for i in range(len(mass_bytes)):
                result_num += mass_bytes[i] * pow(256, i)

        elif byteorder == "little":
            for i in range(len(mass_bytes)):
                result_num += mass_bytes[i] * pow(256, i)

        else:
            logging.error("from_bytes вызван неправильным аргументом byteorder")
            raise TypeError

        return result_num










