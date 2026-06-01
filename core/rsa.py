import math
import secrets
import time
from .utils_for_rsa import *


class key:
    def __init__(self, num1, num2):
        self.degree = num1
        self.module = num2

    def mod_pow(self, num):
        return modular_exp(num, self.degree, self.module)

    def __str__(self):
        return f"({str(self.degree)}, {str(self.module)})"


class RSA:
    def __init__(self, bit_count=16):

        # init data
        if bit_count <= 2:
            raise ValueError("Смешно")

        if bit_count % 2 == 1:
            raise ValueError("Это уже не смешно")

        self.bit_count = bit_count
        self.public_key = None
        self.private_key = None

        self.iter_count = 0

        # generate keys
        flag = self.generate_key()

        while True:
            self.iter_count += 1

            if self.test_for_correctness() and flag:
                break
            else:
                flag = self.generate_key()

    def generate_key(self):
        # generate p and q
        num_p, num_q = gen_two_prime_num(bit_count=self.bit_count // 2)
        num_n = num_p * num_q

        # print((num_n.bit_length() + 7) // 8)
        phi = (num_p - 1) * (num_q - 1)


        # find e
        num_e = secrets.randbelow(phi)
        while gcd(num_e, phi) != 1:
            self.iter_count += 1
            num_e = secrets.randbelow(phi)

        # find d
        x1, x2 = gcdex(phi, num_e)
        num_d = phi - abs(min(x1, x2))

        self.public_key = key(num_e, num_n)
        self.private_key = key(num_d, num_n)

        return num_n.bit_length() == self.bit_count

    def test_for_correctness(self):

        test_code = 1234

        encrypted = modular_exp(test_code, self.public_key.degree, self.public_key.module)
        decrypted = modular_exp(encrypted, self.private_key.degree, self.private_key.module)

        return test_code == decrypted

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key

    def __str__(self):
        return f"{str(self.public_key)}, {str(self.private_key)}"


if __name__ == '__main__':
    pass



