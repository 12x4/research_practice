from core.cipher import cipher
from core.console_app import console_app
from core.rsa import RSA
import logging


class cipher_2(cipher):

    def __init__(self, rsa_key):
        super().__init__(rsa_key)

    def encrypt_to_bytes(self, plaintext):

        enc_text = ""
        list_bytes = []

        for char in plaintext:

            if ord(char) > 255:
                logging.error("Обнаружен символ число которого больше 255")
                return

            list_bytes.append(ord(char))

        mass_bytes = bytearray(list_bytes)
        r = self.from_bytes(mass_bytes)

        if self.key.public_key.module <= r:
            raise ValueError("Слишком маленький ключ для шифрования")

        y = self.key.public_key.mod_pow(r)

        mass_bytes_enc = self.to_bytes(y)


        for char in mass_bytes_enc:
            enc_text += chr(char)

        return enc_text


    def to_bytes(self, num, byteorder="big"):

        result_bytearray = None
        byte_list = []

        while num != 0:
            byte_list.append(num % 256)
            num //= 256

        if byteorder == "big":
            result_bytearray = bytearray(byte_list[::-1])
        elif byteorder == "little":
            result_bytearray = bytearray(byte_list)
        else:
            logging.error("from_bytes вызван неправильным аргументом byteorder")
            raise TypeError

        return result_bytearray

    def from_bytes(self, mass_bytes: bytearray, byteorder="big"):

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

def main():

    test = "abcdefghijklmnopqrstuvwxyz"

    # for i in test:
    #     print(ord(i))
    rsa_key = RSA(256)
    cip = cipher_2(rsa_key)
    print(cip.encrypt_to_bytes(test))


if __name__ == "__main__":
    main()
