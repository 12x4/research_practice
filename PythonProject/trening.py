import math
import secrets
import random


def gcd(a, b) -> int:
    while a % b != 0:
        a, b = b, a % b
    return b


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def phi(n) -> int:
    res = 0
    for i in range(1, n):
        if gcd(i, n) == 1:
            res += 1
    return res


def mod_pow(a, n, m):
    if m == 1: return 0
    r = 1
    a %= m
    while n:
        if n % 2: r = (r * a) % m
        a = (a * a) % m
        n //= 2
    return r


def mp(a, exp, m):
    if m == 1:
        return 0
    r = 1
    a %= m
    while exp:
        if exp % 2:
            r = (r * a) % m
        a = (a ** 2) % m
        exp //= 2
    return r


def diff(a, b, h, p):
    A = mod_pow(h, a, p)
    B = mod_pow(h, b, p)

    k1 = mod_pow(A, a, p)
    k2 = mod_pow(B, b, p)

    print(k1 == k2)


def por_el(a, p):

    for i in range(1, p + 1):
        if a ** i % p == 1:
            print(i)
            break



if __name__ == "__main__":

    print(gcd(10, 6))
    print(egcd(20, 30))
    print(phi(10))
    print(mod_pow(10,2, 9))
    print(mp(10, 1, 6))



