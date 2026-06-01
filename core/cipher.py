import codecs
import math
import random
import secrets
import logging

# from utils_for_rsa import *
# from rsa import RSA

from core.utils import byte_size, xor_for_bytearray
from core.utils_for_rsa import gen_num



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


class cipher_4(cipher_3):

    def __init__(self, rsa_key, meth_before=1, meth_after=1):

        if rsa_key.public_key.module.bit_length() < 9:
            logging.error("Слишком маленький ключ")
            raise ValueError("Слишком маленький ключ")
        super().__init__(rsa_key)

        logging.info(self.key)
        logging.info(self.to_bytes(self.key.public_key.module))
        logging.info(f"meth_before:{meth_before} meth_after:{meth_after}")


        if meth_before not in [1, 2, 3, 4]:
            logging.error('Указан неправильный метод "до", выбран метод 1')
            meth_before = 1

        if meth_after not in [1, 2]:
            logging.error('Указан неправильный метод "после", выбран метод 1')
            meth_after = 1

        self.meth_before = meth_before
        self.meth_after = meth_after

        self.vect_init = None

        # print(byte_size(self.key.public_key.module))
        pass

    # Шифрование блоками
    def encrypt_blocks(self, plaintext):

        block_size = byte_size(self.key.public_key.module) - 1

        # mass_byte = bytearray(plaintext, "utf8")
        mass_byte = bytearray()

        for char in plaintext:
            mass_byte.append(ord(char))

        mass_byte_blocks = []


        for ind in range(0, len(plaintext) // block_size + 1):
            temp_bytes = mass_byte[ind * block_size : (ind + 1) * block_size]
            if len(temp_bytes) == 0:
                continue
            mass_byte_blocks.append(temp_bytes)

        logging.debug(mass_byte_blocks)

        # До шифровки подправляем байты
        temp_list_bytes = []
        match self.meth_before:

            case 1:
                temp_list_bytes = self.proc_group_before_enc_1(mass_byte_blocks, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.proc_group_before_enc_2(mass_byte_blocks, len_block=block_size + 1)

            case 3:
                temp_list_bytes = self.proc_group_before_enc_3(mass_byte_blocks, len_block=block_size + 1)

            case 4:
                temp_list_bytes = self.proc_group_before_enc_4(mass_byte_blocks, len_block=block_size + 1)

            case _:
                logging.error("self.meth_before не стандартный")
                raise ValueError("self.meth_before не стандартный")

        logging.debug(temp_list_bytes)

        temp_list_r = []
        # Конвертируем байты в числа
        for ind in temp_list_bytes:
            temp_list_r.append(self.from_bytes(ind))

        logging.debug(temp_list_r)

        temp_list_y = []
        # Шифруем числа
        for ind in temp_list_r:
            if ind > self.key.public_key.module:
                logging.warning("r больше модуля ключа")
            temp_list_y.append(self.key.public_key.mod_pow(ind))

        logging.debug(temp_list_y)


        # # Пост обработка байтов
        # mass_enc_byte_blocks = []
        #
        # for ind in temp_list_y:
        #     mass_enc_byte_blocks.append(self.to_bytes(ind))

        # После шифровки подправляем байты
        match self.meth_after:

            case 1:
                temp_list_bytes = self.convert_enc_num_to_byte_1(temp_list_y, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.convert_enc_num_to_byte_2(temp_list_y, len_block=block_size + 1)

            case _:
                logging.error("self.meth_after не стандартный")
                raise ValueError("self.meth_after не стандартный")

        logging.debug(temp_list_bytes)

        # Конверт в строку
        enc_text = ""

        for ind in temp_list_bytes:
            for _byte in ind:
                enc_text += chr(_byte)

        logging.info(f"Закончил шифровку {plaintext}")
        return enc_text

    # Расшифровка блоками
    def decrypt_blocks(self, ciphertext):

        block_size = byte_size(self.key.private_key.module) - 1

        # Конверт строки в массив байтов
        mass_byte = bytearray()
        for char in ciphertext:
            mass_byte.append(ord(char))

        logging.debug(mass_byte)

        # До расшифровки подправляем байты
        temp_list_bytes = []
        match self.meth_after:

            case 1:
                temp_list_bytes = self.reverse_convert_enc_num_to_byte_1(mass_byte, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.reverse_convert_enc_num_to_byte_2(mass_byte, len_block=block_size + 1)

            case _:
                logging.error("self.meth_after не стандартный")
                raise ValueError("self.meth_after не стандартный")

        logging.debug(temp_list_bytes)

        temp_list_y = []
        # Конвертируем байты в числа
        for ind in temp_list_bytes:
            temp_list_y.append(self.from_bytes(ind))

        logging.debug(temp_list_y)

        temp_list_r = []
        # Расшифруем числа
        for ind in temp_list_y:
            temp_list_r.append(self.key.private_key.mod_pow(ind))

        logging.debug(temp_list_r)

        # Пост обработка байтов
        mass_byte_blocks = []

        for ind in temp_list_r:
            mass_byte_blocks.append(self.to_bytes(ind))

        logging.debug(mass_byte_blocks)

        # После расшифровки подправляем байты
        match self.meth_before:

            case 1:
                temp_list_bytes = self.reverse_proc_group_before_enc_1(mass_byte_blocks, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.reverse_proc_group_before_enc_2(mass_byte_blocks, len_block=block_size + 1)

            case 3:
                temp_list_bytes = self.reverse_proc_group_before_enc_3(mass_byte_blocks, len_block=block_size + 1)

            case 4:
                temp_list_bytes = self.reverse_proc_group_before_enc_4(mass_byte_blocks, len_block=block_size + 1)

            case _:
                logging.error("self.meth_before не стандартный")
                raise ValueError("self.meth_before не стандартный")

        logging.debug(temp_list_bytes)

        # Конверт в строку
        enc_text = ""

        for ind in temp_list_bytes:
            for _byte in ind:
                enc_text += chr(_byte)

        logging.info(f"Закончил расшифровку {enc_text}")
        return enc_text

    # Обработка групп перед шифрованием метод 1
    def proc_group_before_enc_1(self, mass_byte_blocks, len_block=None):
        return mass_byte_blocks

    # Обработка групп перед шифрованием метод 2
    def proc_group_before_enc_2(self, mass_byte_blocks, len_block=None):
        temp_byte = int(self.to_bytes(self.key.public_key.module)[0])



        for ind in range(0, len(mass_byte_blocks) - 1):
            mass_byte_blocks[ind].insert(0, random.randint(1,temp_byte - 1))

        # В конец добавляю k тый байт который показывает сколько байтов после и вместе с ним надо снести
        # Если до k того байта можно добавить еще пару байтов добавляются единички

        len_block = len(self.to_bytes(self.key.public_key.module))
        _raz = len_block - len(mass_byte_blocks[-1])
        _bytes = bytearray([random.randint(1, 255)] * (_raz - 1))
        _bytes.append(_raz)
        mass_byte_blocks[-1] = mass_byte_blocks[-1][::-1]
        mass_byte_blocks[-1] += _bytes
        mass_byte_blocks[-1] = mass_byte_blocks[-1][::-1]

        return mass_byte_blocks

    # Обработка групп перед шифрованием метод 3
    def proc_group_before_enc_3(self, mass_byte_blocks, len_block=None):

        if len_block is None:
            len_block = len(mass_byte_blocks[0])

        # Генерация вектора инициализации gen_bun получает количество битов
        init_vector = self.to_bytes(gen_num(len_block * 8))
        new_mass_byte_blocks = [xor_for_bytearray(init_vector, ind) for ind in mass_byte_blocks]

        # Надо еще как-то возвращать вектор инициализации
        self.vect_init = init_vector
        return new_mass_byte_blocks

    # Обработка групп перед шифрованием метод 4
    def proc_group_before_enc_4(self, mass_byte_blocks, len_block=None):

        if len_block is None:
            len_block = len(mass_byte_blocks[0])

        # Генерация вектора инициализации gen_bun получает количество битов
        init_vector = self.to_bytes(gen_num(len_block // 2 * 8))
        new_mass_byte_blocks = []

        # Для нечетной длины блока
        len_counter = len_block // 2
        if len_block % 2 == 1:
            len_counter += 1

        # Для знания предела
        max_counter = 256 ** len_counter
        counter = -1

        for ind in mass_byte_blocks:

            # Вычисляем новый вектор
            counter += 1
            if counter > max_counter:
                raise ValueError("Counter пересек черту бедности")
            new_init_vector = init_vector + self.to_bytes(counter, byte_count=len_counter)

            # ИКСОРИМ
            new_mass_byte_blocks.append(xor_for_bytearray(new_init_vector, ind))

        # Надо еще как-то возвращать вектор инициализации
        self.vect_init = init_vector
        return new_mass_byte_blocks

    # Преобразование зашифрованного числа в массив байтов метод 1
    def convert_enc_num_to_byte_1(self, enc_num_list: list, len_block: int=None) -> list:

        if len_block is None:
            logging.error("Плохо что нет len_block")
            raise Exception("Плохо что нет len_block")

        result_list = []

        for ind in enc_num_list:
            bytes = self.to_bytes(ind, byte_count=len_block)
            result_list.append(bytes)

        return result_list

    # Преобразование зашифрованного числа в массив байтов метод 2
    def convert_enc_num_to_byte_2(self, enc_num_list: list, len_block: int=None) -> list:

        result_list = []

        # Добавляем в конец байт блоков их длину

        for ind in enc_num_list:
            bytes = self.to_bytes(ind)
            bytes.append(len(bytes))
            result_list.append(bytes)

        return result_list

    # 77777777777777777777777777
    # ОБРАТНЫЕ ФУНКЦИИ К ВЕРХНИМ
    # 77777777777777777777777777

    def reverse_proc_group_before_enc_1(self, mass_byte_blocks: list, len_block=None) -> list:
        return mass_byte_blocks

    def reverse_proc_group_before_enc_2(self, mass_byte_blocks: list, len_block=None) -> list:

        result_list = []

        for ind in mass_byte_blocks[:-1]:
            ind.pop(0)
            result_list.append(ind)

        _count = int(mass_byte_blocks[-1][0])
        for ji in range(_count):
            mass_byte_blocks[-1].pop(0)
        result_list.append(mass_byte_blocks[-1])

        return result_list

    def reverse_proc_group_before_enc_3(self, mass_byte_blocks: list, len_block=None) -> list:

        if self.vect_init is None:
            raise Exception("self.vect_init равен None")

        new_mass_byte_blocks = [xor_for_bytearray(self.vect_init, ind) for ind in mass_byte_blocks]
        return new_mass_byte_blocks

    def reverse_proc_group_before_enc_4(self, mass_byte_blocks: list, len_block=None) -> list:
        if len_block is None:
            len_block = len(mass_byte_blocks[0])

        if self.vect_init is None:
            raise Exception("self.vect_init равен None")

        # Генерация вектора инициализации gen_bun получает количество битов
        new_mass_byte_blocks = []

        # Для нечетной длины блока
        len_counter = len_block // 2
        if len_block % 2 == 1:
            len_counter += 1

        # Для знания предела
        max_counter = 256 ** len_counter
        counter = -1

        for ind in mass_byte_blocks:

            # Вычисляем новый вектор
            counter += 1
            if counter > max_counter:
                raise ValueError("Counter пересек черту бедности")
            new_init_vector = self.vect_init + self.to_bytes(counter, byte_count=len_counter)

            # ИКСОРИМ
            new_mass_byte_blocks.append(xor_for_bytearray(new_init_vector, ind))

        # Надо еще как-то возвращать вектор инициализации
        return new_mass_byte_blocks

    def reverse_convert_enc_num_to_byte_1(self, mass_byte_blocks: bytearray, len_block: int) -> list:

        # Делим список байтов на блоки по k = byte_size(n)
        result_list = []
        block_count = len(mass_byte_blocks) // len_block

        for ind in range(block_count):
            result_list.append(mass_byte_blocks[ ind * len_block : (ind + 1) * len_block])

        # Хитрый алгоритм
        if block_count * len_block < len(mass_byte_blocks):
            result_list.append(mass_byte_blocks[block_count * len_block:])

        return result_list

    def reverse_convert_enc_num_to_byte_2(self, mass_byte: bytearray, len_block: int) -> list:

        result_list = []

        # Переворачиваем массив
        mass_byte = mass_byte[::-1]
        len_mass_byte = len(mass_byte)
        ind = 0

        # Собираем как бы перевернутые блоки
        while ind < len_mass_byte:

            # Берем байт который говорит сколько байтов перед ним являются одним числом
            _ind = int(mass_byte[ind])
            _mass = bytearray()

            # Добавляем эти числа от конца получается сразу перевернутые
            while _ind > 0:
                _mass.append(mass_byte[ind + _ind])
                _ind -= 1

            # Получаем список чисел, но это перевернутый список
            result_list.append(_mass)
            ind += int(mass_byte[ind]) + 1

        # Возвращаем переворачивая
        return result_list[::-1]


class cipher_5(cipher_4):

    def __init__(self, rsa, method_before=1, method_after=1, encoding="utf-8"):
        super().__init__(rsa, method_before, method_after)

        try:
            codecs.getencoder(encoding)
        except LookupError as e:
            logging.error(f"{e}\nНеправильная кодировка")
            print("Неправильная кодировка")
            exit(1)

        self.encoding = encoding

    # Шифрование блоками
    def encrypt_blocks(self, plaintext):

        block_size = byte_size(self.key.public_key.module) - 1

        # mass_byte = bytearray(plaintext, "utf8")
        # mass_byte = bytearray()

        mass_byte = bytearray(plaintext, self.encoding)

        mass_byte_blocks = []

        for ind in range(0, len(plaintext) // block_size + 1):
            temp_bytes = mass_byte[ind * block_size: (ind + 1) * block_size]
            if len(temp_bytes) == 0:
                continue
            mass_byte_blocks.append(temp_bytes)

        logging.debug(mass_byte_blocks)

        # До шифровки подправляем байты
        temp_list_bytes = []
        match self.meth_before:

            case 1:
                temp_list_bytes = self.proc_group_before_enc_1(mass_byte_blocks, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.proc_group_before_enc_2(mass_byte_blocks, len_block=block_size + 1)

            case 3:
                temp_list_bytes = self.proc_group_before_enc_3(mass_byte_blocks, len_block=block_size + 1)

            case 4:
                temp_list_bytes = self.proc_group_before_enc_4(mass_byte_blocks, len_block=block_size + 1)

            case _:
                logging.error("self.meth_before не стандартный")
                raise ValueError("self.meth_before не стандартный")

        logging.debug(temp_list_bytes)

        temp_list_r = []
        # Конвертируем байты в числа
        for ind in temp_list_bytes:
            temp_list_r.append(self.from_bytes(ind))

        logging.debug(temp_list_r)

        temp_list_y = []
        # Шифруем числа
        for ind in temp_list_r:
            if ind > self.key.public_key.module:
                logging.warning("r больше модуля ключа")
            temp_list_y.append(self.key.public_key.mod_pow(ind))

        logging.debug(temp_list_y)

        # # Пост обработка байтов
        # mass_enc_byte_blocks = []
        #
        # for ind in temp_list_y:
        #     mass_enc_byte_blocks.append(self.to_bytes(ind))

        # После шифровки подправляем байты
        match self.meth_after:

            case 1:
                temp_list_bytes = self.convert_enc_num_to_byte_1(temp_list_y, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.convert_enc_num_to_byte_2(temp_list_y, len_block=block_size + 1)

            case _:
                logging.error("self.meth_after не стандартный")
                raise ValueError("self.meth_after не стандартный")

        logging.debug(temp_list_bytes)

        # Конверт в строку
        enc_text = ""

        for ind in temp_list_bytes:
            for _byte in ind:
                enc_text += chr(_byte)

        logging.info(f"Закончил шифровку {plaintext}")
        return enc_text

    # Расшифровка блоками
    def decrypt_blocks(self, ciphertext):

        block_size = byte_size(self.key.private_key.module) - 1

        # Конверт строки в массив байтов
        mass_byte = bytearray()
        for char in ciphertext:
            mass_byte.append(ord(char))

        logging.debug(mass_byte)

        # До расшифровки подправляем байты
        temp_list_bytes = []
        match self.meth_after:

            case 1:
                temp_list_bytes = self.reverse_convert_enc_num_to_byte_1(mass_byte, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.reverse_convert_enc_num_to_byte_2(mass_byte, len_block=block_size + 1)

            case _:
                logging.error("self.meth_after не стандартный")
                raise ValueError("self.meth_after не стандартный")

        logging.debug(temp_list_bytes)

        temp_list_y = []
        # Конвертируем байты в числа
        for ind in temp_list_bytes:
            temp_list_y.append(self.from_bytes(ind))

        logging.debug(temp_list_y)

        temp_list_r = []
        # Расшифруем числа
        for ind in temp_list_y:
            temp_list_r.append(self.key.private_key.mod_pow(ind))

        logging.debug(temp_list_r)

        # Пост обработка байтов
        mass_byte_blocks = []

        for ind in temp_list_r:
            mass_byte_blocks.append(self.to_bytes(ind))

        logging.debug(mass_byte_blocks)

        # После расшифровки подправляем байты
        match self.meth_before:

            case 1:
                temp_list_bytes = self.reverse_proc_group_before_enc_1(mass_byte_blocks, len_block=block_size + 1)

            case 2:
                temp_list_bytes = self.reverse_proc_group_before_enc_2(mass_byte_blocks, len_block=block_size + 1)

            case 3:
                temp_list_bytes = self.reverse_proc_group_before_enc_3(mass_byte_blocks, len_block=block_size + 1)

            case 4:
                temp_list_bytes = self.reverse_proc_group_before_enc_4(mass_byte_blocks, len_block=block_size + 1)

            case _:
                logging.error("self.meth_before не стандартный")
                raise ValueError("self.meth_before не стандартный")

        logging.debug(temp_list_bytes)

        # Конверт в строку
        enc_text = ""

        for ind in temp_list_bytes:
            # for _byte in ind:
            #     enc_text += chr(_byte)
            enc_text += ind.decode(self.encoding)

        logging.info(f"Закончил расшифровку {enc_text}")
        return enc_text




