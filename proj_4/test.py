import random
from core.cipher import cipher_4
from core.rsa import RSA
import codecs

# from core.utils_for_rsa import gen_two_prime_num
# from core.cipher import cipher_3
# from core.rsa import RSA
#
# # num_p, num_q = gen_two_prime_num(bit_count=2)
# # num_n = num_p * num_q
# #
# # print(f"{num_p} \t{num_p.bit_length()}")
# # print(f"{num_q} \t{num_q.bit_length()}")
# # print(f"{num_n} \t{num_n.bit_length()}")
#
# rsa = RSA(16)
#
# n = 256
# cip = cipher_3(rsa)
# print(cip.to_bytes(n))

# a = codecs.getencoder("windows-1251")
# print(a)


rsa = RSA(16)
a = cipher_4(rsa)

num = 258

b1 = a.to_bytes(num, 5)
print(b1)
b2 = a.from_bytes(b1)
print(b2)







