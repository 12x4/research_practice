from cProfile import label
from random import getrandbits, randint
import time
import matplotlib.pyplot as plt
import random

def gcd(a, b, i=1):

    while a%b!=0:

        a, b = b, a % b
        i += 1

    return b


def new_randint(k):
    return randint(2 ** (k - 1), 2 ** k - 1)


def new_getrandbits(k):
    return getrandbits(k) | (2 ** (k - 1))


def new_randint_2(k):
    return new_randint(k) | 1

def new_getrandbits_2(k):
    return new_getrandbits(k) | 1


def main():
    num = 4
    n1, n2 = new_randint(num), new_getrandbits(num)
    print(n1, n2)
    print(f"gcd={gcd(n1, n2)} ")

    x_lab = [10, 50, 100, 200, 500, 1000, 2000]
    time_gcd = []
    time_gcd_ev = []

    for n in x_lab:
        start = time.time()
        result = new_randint(n)
        stop = time.time()
        time_gcd_t = stop - start
        time_gcd.append(time_gcd_t)

        start = time.time()
        res_x = new_getrandbits(n)
        stop = time.time()
        time_gcd_ev_t = stop - start
        time_gcd_ev.append(time_gcd_ev_t)

        print(f"Размер: {n} цифр - randint {time_gcd_t}, getrandbits:{time_gcd_ev_t}")

    plt.plot(x_lab, time_gcd, label="randint")
    plt.legend()
    plt.plot(x_lab, time_gcd_ev, label="randbits")
    plt.legend()

    plt.xlabel("Количество цифр")
    plt.ylabel("Время в микросекундах")
    plt.show()


if __name__ == "__main__":
    main()
