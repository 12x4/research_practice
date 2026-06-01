import random
import secrets


# random.seed()
# for _ in range(3):
#     print(random.random())

# for _ in range(3):
#     print(secrets.randbelow(10000)/10000.0)

# num = secrets.randbits(3)
# print(num)

# otp_code = secrets.randbits(20)
# print(otp_code)

# token = secrets.token_bytes(1)
# print(token)

# integer_value = int.from_bytes(secrets.token_bytes(16), byteorder='big')
# print(integer_value)

def euler(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n = n // p
            result = result * (1 - (1 / float(p)))
        p = p + 1
    if n > 1:
        result -= result // n
    return int(result)

for n in range(1, 7001):
    print("число эйлера", n, ":", euler(n))