import secrets
import math


def gen_num(bit_count=16):
    num = secrets.randbits(bit_count)
    num = num | (1 << (bit_count - 1))
    num |= 1
    return num


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def gcdex(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return x0, y0


def modular_exp(a, b, n):

    # ai = 1
    # a = a % n
    # while b > 0:
    #     if b & 1:
    #         ai = (ai * a) % n
    #     b = b >> 1
    #     a = a ** 2 % n

    # return ai
    return pow(a, b, n)

def gen_two_prime_num(bit_count=16):

    num1 = None
    while True:
        num1 = gen_num(bit_count)
        if miller_rabin(num1):
            break

    num2 = None
    while True:
        num2 = gen_num(bit_count)
        if miller_rabin(num2):
            break


    if num1 == num2:
            return gen_two_prime_num(bit_count)

    return num1, num2


def miller_rabin(n, k=100):
    if n == 3 or n == 2:
        return True
    # Find r and d such that n-1 = 2^r * d
    # a^((2^r)) =:= -1 mod N
    #
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    # Run the test k times
    for _ in range(k):
        a = secrets.randbelow(n - 4) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True




