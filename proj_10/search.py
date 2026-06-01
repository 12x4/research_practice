from pyexpat.errors import messages

import matplotlib.pyplot as plt
import time

from core.rsa import RSA
from core.diffic import DiffHell
from core.cipher import cipher_5
from core.utils import byte_size


class search():
    def __init__(self):

        self.list_bits = [16, 32, 64, 128, 196]

        pass

    def search_work_time(self, flag=True):

        times_rsa = []

        for ind in self.list_bits:
            times_rsa.append(self.wrapper_rsa_time(ind))

        plt.plot([5, 10, 15, 18, 30], self.list_bits, color="red", label="rsa")

        plt.xlabel("Количество итераций")
        plt.ylabel("Количество бит")

    def search_iter_count(self):

        iter_rsa = []

        for ind in self.list_bits:
            a = RSA(ind)
            iter_rsa.append(a.iter_count)

        plt.plot(iter_rsa, self.list_bits, color="red", label="rsa")

        plt.xlabel("Количество итераций")
        plt.ylabel("Количество бит")

        pass

    def search_key_size(self):

        key_size_rsa = []

        for ind in self.list_bits:
            a = RSA(ind)
            ind_size = 0
            ind_size += byte_size(a.public_key.module)
            ind_size += byte_size(a.public_key.degree)
            ind_size += byte_size(a.private_key.degree)
            key_size_rsa.append(ind_size)

        plt.plot(key_size_rsa, self.list_bits, color="red", label="rsa")
        plt.xlabel("Размер ключа(байты)")
        plt.ylabel("Количество бит")

    def search_memory_save(self):

        gg_11 = []
        gg_12 = []
        gg_21 = []
        gg_22 = []
        gg_31 = []
        gg_32 = []
        gg_41 = []
        gg_42 = []

        message = open("data/sei-cert.txt", "r+").read()


        for ind in self.list_bits:

            key = RSA(ind)

            gg_11.append(len(cipher_5(key, 1,1).encrypt_blocks(message)))
            gg_12.append(len(cipher_5(key, 1,2).encrypt_blocks(message)))
            gg_21.append(len(cipher_5(key, 2,1).encrypt_blocks(message)))
            gg_22.append(len(cipher_5(key, 2,2).encrypt_blocks(message)))
            gg_31.append(len(cipher_5(key, 3,1).encrypt_blocks(message)))
            gg_32.append(len(cipher_5(key, 3,2).encrypt_blocks(message)))

            try:
                gg_41.append(len(cipher_5(key, 4,1).encrypt_blocks(message)))
            except Exception as e:
                gg_41.append(0)

            try:
                gg_42.append(len(cipher_5(key, 4,2).encrypt_blocks(message)))
            except Exception as e:
                gg_42.append(0)


        plt.plot(gg_11, self.list_bits, color="red", linestyle="-", label="11")
        plt.plot(gg_12, self.list_bits, color="green", linestyle="--", label="12")
        plt.plot(gg_11, self.list_bits, color="black", linestyle="-.", label="21")
        plt.plot(gg_11, self.list_bits, color="blue", linestyle=":", label="22")
        plt.plot(gg_11, self.list_bits, color="purple", linestyle="solid", label="31")
        plt.plot(gg_11, self.list_bits, color="yellow", linestyle="dashed", label="32")
        plt.plot(gg_11, self.list_bits, color="orange", linestyle="dashdot", label="41")
        plt.plot(gg_11, self.list_bits, color="white", linestyle="dotted", label="42")

        plt.xlabel("Размер зашифрованного файла(байты)")
        plt.ylabel("Количество бит")

    def wrapper_rsa_time(self, bit_count):

        start = time.perf_counter()

        RSA(bit_count=bit_count)

        end = time.perf_counter()

        return end - start

    def wrapper_dh_time(self, bit_count):

        start = time.perf_counter()

        Alice = DiffHell(bit_count=bit_count)
        Alice.gen_pg()

        # bob получает p и g
        Bob = DiffHell(pg=Alice.get_pg())

        # Генерируют часть ключей
        Alice.gen_part_key()
        Bob.gen_part_key()

        Alice.proc_key(Bob.get_part_key())
        Bob.proc_key(Alice.get_part_key())

        end = time.perf_counter()

        return end - start



if __name__ == "__main__":
    opa = search()

    # Для запуска выбрать одно из

    opa.search_work_time()
    # opa.search_iter_count()
    # opa.search_key_size()
    # opa.search_memory_save()

    plt.grid()
    plt.legend()
    plt.show()









