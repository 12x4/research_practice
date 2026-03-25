from string import punctuation

from fontTools.misc.eexec import decrypt

from core.cipher import cipher_2
from core.rsa import RSA

import logging
import time
import math


class cipher_3(cipher_2):

    def __init__(self, rsa_key, file_words="google-10000-english.txt"):
        super().__init__(rsa_key)
        self.file_words = file_words
        self.list_words = None

        # Средняя длина слов в байтах
        self.average_word_length = 6.587

        self.punctuation_dict = [" ", ", ", ". ", "! ", "? "]

    def dict_attack_1(self, encrypted_text, byte_count):

        mass_bytes_enc = self.str_to_bytes(encrypted_text)
        y = self.from_bytes(mass_bytes_enc)
        r = None

        for num in range(pow(256, byte_count)):

            if self.key.public_key.mod_pow(num) == y:
                print(f"R it`s find: {num}")
                r = num
                break

        mass_bytes = self.to_bytes(r)
        decrypt_text = self.bytes_to_str(mass_bytes)

        return decrypt_text

    def dict_attack_2(self, encrypted_text, byte_count):

        mass_bytes_enc = self.str_to_bytes(encrypted_text)
        y = self.from_bytes(mass_bytes_enc)

        encrypted_text = None

        # abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,.?!"
        abc = "|abcdefghijklmnopqrstuvwxyz ,.?!"

        # Должен был стать одним из методов решения проблемы
        # Но оказалось что если в начало алфавита добавить ненужный символ то баг фиксится

        # for num in range(byte_count):
        #
        #     mass_bytes = self.to_bytes(0, byte_count=num + 1, abc=abc)
        #     r = self.from_bytes(mass_bytes)
        #
        #     if self.key.public_key.mod_pow(r) == y:
        #         encrypted_text = self.bytes_to_str(self.to_bytes(0, byte_count=num + 1, abc=abc))
        #         print(f"Text it`s find: {encrypted_text}")
        #         return encrypted_text

        for num in range(pow(len(abc), byte_count)):

            mass_bytes = self.to_bytes(num, abc=abc)
            r = self.from_bytes(mass_bytes)

            if self.key.public_key.mod_pow(r) == y:
                encrypted_text = self.bytes_to_str(self.to_bytes(num, abc=abc))
                print(f"Text it`s find: {encrypted_text}")
                return encrypted_text

        return encrypted_text

    def dict_attack_3(self, encrypted_text, byte_count):

        if not self.loading_dict():
            return

        mass_bytes_enc = self.str_to_bytes(encrypted_text)
        y = self.from_bytes(mass_bytes_enc)

        approximate_word_count = int((byte_count // self.average_word_length) + 2)

        for num in range(pow(len(self.list_words), approximate_word_count)):

            # Тут создается массив слов на проверку
            text_words = self.super_func(num, abc=self.list_words)

            for num_2 in range(pow(len(self.punctuation_dict), len(text_words) - 1)):

                # Тут создается массив знаков препинаний которые могут быть между словами
                punctuation_words = self.super_func(num_2, abc=self.punctuation_dict)

                # Сам текст соединяется из двух массивом слов и знаков препинаний
                text = "".join(self.super_func_2(text_words, punctuation_words))

                # Отправляем текст на up символов стоящих после точки, и первого символа
                text = self.super_func_3(text)

                # Это для того чтобы в конце был символ
                for char_punc in ".!?":

                    temp_text = text + char_punc

                    mass_bytes = self.str_to_bytes(temp_text)
                    r = self.from_bytes(mass_bytes)

                    if self.key.public_key.mod_pow(r) == y:
                        print(f"Text it`s find: {temp_text}")
                        return temp_text

    # Это как бы функция для перевода чисел из 10 ричного в k ичное
    # k = len(abc)
    def super_func(self, num: int, byte_count=None, byteorder="big", abc=None) -> list:

        word_list = []
        abc_len = len(abc)

        if num == 0:
            word_list.append(abc[0])

        while num != 0:
            word_list.append(abc[num % abc_len])
            num //= abc_len

        if byte_count is not None and len(word_list) < byte_count:
            for _ in range(byte_count - len(word_list)):
                word_list.append(ord(abc[0]))

        if byteorder == "big":
            word_list = word_list[::-1]
        elif byteorder == "little":
            pass
        else:
            logging.error("from_bytes вызван неправильным аргументом byteorder")
            raise TypeError

        return word_list

    # Эта функция для объединения двух списков по принципу слоеный пирог
    def super_func_2(self, list_1, list_2):
        result_list = []

        for num in range(max(len(list_1), len(list_2))):

            if num < len(list_1):
                result_list.append(list_1[num])

            if num < len(list_2):
                result_list.append(list_2[num])

        return result_list

    # Эта функция up ет символы стоящие после точки, и первый символ
    def super_func_3(self, text):
        result = []
        capitalize_next = True  # первая буква должна быть заглавной

        for ch in text:
            if capitalize_next and ch.isalpha():
                result.append(ch.upper())
                capitalize_next = False
            else:
                result.append(ch)

            if ch in ".!?":
                capitalize_next = True
            elif ch.isalpha():
                capitalize_next = False

        return "".join(result)

    def loading_dict(self):

        try:
            self.list_words = [""]
            with open(self.file_words, "r+") as f:

                self.list_words += f.read().split("\n")
            return True

        except Exception as e:
            self.list_words = []
            logging.error(f"Не удалось прочитать file_words \n{e}")
            return False


def main():
    test = "The best!"

    # for i in test:
    #     print(ord(i))
    rsa_key = RSA(64)
    cip = cipher_3(rsa_key)
    print(rsa_key.public_key)

    encrypted_text = cip.encrypt_to_bytes(test)
    print(encrypted_text)
    # print(cip.dict_attack_1(encrypted_text, len(test)))
    cip.dict_attack_3(encrypted_text, len(test))

    # cip.loading_dict()
    # num = 0
    # for i in cip.list_words:
    #     num += len(i)
    #
    # print(num / len(cip.list_words))

if __name__ == "__main__":
    main()





