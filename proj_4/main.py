from core.cipher import cipher_3
from core.rsa import RSA

import math
import logging
import random

from core.utils import byte_size, xor_for_bytearray
from core.utils_for_rsa import gen_num

logging.basicConfig(
    level=logging.DEBUG, # Уровень: логируются INFO и выше
    filename="app.log",  # Файл для записи
    filemode="w",        # "w" - перезапись, "a" - добавление
    format="%(asctime)s - %(levelname)s - %(message)s" # Формат времени и текста
)


class cipher_4(cipher_3):

    def __init__(self, rsa_key, meth_before=1, meth_after=1):

        if rsa_key.public_key.module.bit_length() < 16:
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

        if plaintext == "":
            return bytearray()

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

        if len(ciphertext) == 0:
            return ""

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


def main():

    key = RSA(32)
    cip = cipher_4(key, 3, 1)

    text = "cha-cha-20"

    enc_text = cip.encrypt_blocks(text)
    print(enc_text, len(enc_text))
    temp_text = cip.decrypt_blocks(enc_text)

    print(temp_text)


if __name__ == "__main__":
    main()