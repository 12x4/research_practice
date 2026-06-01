import logging
import os
from sympy import factorint
import secrets

from core.utils_for_rsa import *
from core.utils import *


class DiffHell:

    def __init__(self, pg=None, bit_count=32):

        if bit_count < 8:
            raise ValueError("Лучше так не делать")

        if pg is None:
            self.p = None
            self.g = None
        else:
            self.p = pg[0]
            self.g = pg[1]

        self.part_key = None
        self.key = None
        self.bit_count = bit_count

        pass

    def gen_pg(self):

        # генерация p
        num1 = None
        while True:
            num1 = gen_num(self.bit_count)
            if isprime(num1) and num1.bit_length() == self.bit_count:
                break
        self.p = num1

        # генерация g
        phi = self.p - 1
        factor = factorint(phi)
        prime_divisors = factor.keys()
        # print(prime_divisors)

        while True:

            candidate_num = secrets.randbelow(phi -  3) + 2
            flag = True

            for ind in prime_divisors:
                if pow(candidate_num, phi//ind, self.p) == 1:
                    flag = False
                    break

            if flag:
                self.g = candidate_num
                break


    def get_pg(self):
        return self.p, self.g

    def gen_part_key(self):
        self.part_key = secrets.randbelow(self.p - 2) + 2

    def get_part_key(self):
        if self.part_key is None:
            raise ValueError("Сначала сгенерируйте часть ключа!")

        return  pow(self.g, self.part_key, self.p)

    def proc_key(self, _part_key):

        if type(_part_key) != int:
            raise ValueError("Произошла какая то ошибка, тип полученного объекта не int")

        self.key = pow(_part_key, self.part_key, self.p)

    def encrypt(self, text):
        return

    def decrypt(self, plaintext):
        return
