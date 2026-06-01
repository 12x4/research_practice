import time
import matplotlib.pyplot as plt

def fast_power(a, b):
    arr = bin(b)[3:]
    ai = a
    for i in arr:
        if i == "0":
            ai = ai ** 2
        if i == "1":
            ai = (ai ** 2) * a
    return ai

def modular_exp(a, b, n):

    ai = 1
    a = a % n
    while b > 0:
        if b & 1:
            ai = (ai * a) % n
        b = b >> 1
        a = a ** 2 % n

    return ai


def main():
    labels = ["fast_power", "modular_exp"]
    times = []
    start = time.time()
    print(fast_power(7, 256) % 13)
    stop = time.time()
    times.append(stop - start)

    start = time.time()
    print(modular_exp(7, 256, 13))
    stop = time.time()
    times.append(stop - start)

    plt.bar(labels, times, label="Время работы функции")  # bins - количество столбцов
    plt.ylabel("Время микросекунды")
    plt.title("Простая гистограмма")
    plt.legend()
    plt.show()



if __name__ == "__main__":
    main()

