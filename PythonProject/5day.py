import time
import matplotlib.pyplot as plt
from random import getrandbits, randint


def modular_exp(a, b, n):

    ai = 1
    a = a % n
    while b > 0:
        if b & 1:
            ai = (ai * a) % n
        b = b >> 1
        a = a ** 2 % n

    return ai

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def new_getrandbits(k):
    return getrandbits(k) | (2 ** (k - 1))

def prime(k):
    num = new_getrandbits(k)
    while is_prime(num) is False:
        num = new_getrandbits(k)
    return num

def hell(a, b, p, g):

    print(f"a={a} b={b} p={p} g={g}")

    A = modular_exp(g, a, p)
    B = modular_exp(g, b, p)

    print(f"A={A} B={B}")

    k1 = modular_exp(A, b, p)
    k2 = modular_exp(B, a, p)

    print(f"k1={k1} k2={k2}")

    if k1 == k2:
        print("Sucsesfull")
    else:
        print("error")

def main():
    x_lab = [2, 4, 8, 16, 32, 42, 46]
    times = []

    a = randint(10, 100)
    b = randint(10, 100)

    for n in x_lab:
        start = time.time()
        hell(a, b, prime(n), getrandbits(n))
        stop = time.time()
        time_gcd_t = stop - start
        times.append(time_gcd_t)

        print(f"Размер: {n} цифр - время {time_gcd_t}")
        print()

    plt.plot(x_lab, times, label="hellman")
    plt.legend()

    plt.xlabel("Количество цифр")
    plt.ylabel("Время в микросекундах")
    plt.show()



if __name__ == "__main__":
    main()
