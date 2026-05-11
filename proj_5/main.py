from fontTools.misc.eexec import decrypt

from core.cipher import cipher_4
from core.rsa import RSA

import math
import logging
import random
import codecs

from core.utils import byte_size, xor_for_bytearray
from core.utils_for_rsa import gen_num

logging.basicConfig(
    level=logging.DEBUG, # Уровень: логируются INFO и выше
    filename="app.log",  # Файл для записи
    filemode="w",        # "w" - перезапись, "a" - добавление
    format="%(asctime)s - %(levelname)s - %(message)s" # Формат времени и текста
)


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

if __name__ == "__main__":
    rsa = RSA(32)

    cipher = cipher_5(rsa, encoding="windows-1251")

    text = "KAMIL KAMIL KAMIL KAMIL KAMIL"

    encrypt = cipher.encrypt_blocks(text)
    print(encrypt)

    decrypt = cipher.decrypt_blocks(encrypt)
    print(decrypt)





