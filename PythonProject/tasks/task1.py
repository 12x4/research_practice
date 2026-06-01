import secrets
import random
import time
import matplotlib.pyplot as plt


def generate_randbits(k, h=False):
    num = secrets.randbits(k)

    if h:
        return num | 1 | (1 << (k - 1))
    return num | (1 << (k - 1))


def generate_randbelow(k, h=False):
    num = secrets.randbelow(1 << k)

    if h:
        return num | 1 | (1 << k - 1) | 1
    return num | (1 << k - 1) | 1


def generate_token_bytes(k, h=False):
    bytes = (k + 7) // 8
    num = int.from_bytes(secrets.token_bytes(bytes), 'big')
    num &= (1 << k) - 1

    if h:
        return num | 1 | (1 << (k - 1))
    return num | (1 << (k - 1))


def compare_bits(k_sequence):
    methods = [
        ("randbits", generate_randbits),
        ("randbelow", generate_randbelow),
        ("token_bytes", generate_token_bytes)
    ]

    results = {name: [] for name, _ in methods}

    for k in k_sequence:
        for name, method in methods:
            start = time.time()
            method(k)
            end = time.time()
            results[name].append(end - start)

    print(results)

    plt.figure(figsize=(10, 6))
    for name, times in results.items():
        plt.plot(k_sequence, times, label=name, marker='o')

    plt.title("Сравнение методов secrets")
    plt.xlabel("Битность k")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.grid(True)
    plt.show()


def random_getrandbits(k):
        return random.getrandbits(k)
def random_randint(k):
        return random.randint(0, (1 << k) - 1)


def compare_with_random_1(k_sequence):

    methods = [
        ("secrets.randbits", generate_randbits),
        ("random.getrandbits", random_getrandbits)
    ]

    results = {name: [] for name, _ in methods}

    for k in k_sequence:
        for name, method in methods:
            start = time.time()
            method(k)
            end = time.time()
            results[name].append(end - start)

    plt.figure(figsize=(10, 6))
    for name, times in results.items():
        plt.plot(k_sequence, times, label=name, marker='s')

    plt.title("Secrets и Random")
    plt.xlabel("Битность k")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.grid(True)
    plt.show()


def compare_with_random_2(k_sequence):
    methods = [
        ("secrets.randbelow", generate_randbelow),
        ("random.randint", random_randint)
    ]

    results = {name: [] for name, _ in methods}

    for k in k_sequence:
        for name, method in methods:
            start = time.time()
            method(k)
            end = time.time()
            results[name].append(end - start)

    plt.figure(figsize=(10, 6))
    for name, times in results.items():
        plt.plot(k_sequence, times, label=name, marker='s')

    plt.title("Secrets и Random")
    plt.xlabel("Битность k")
    plt.ylabel("Время (сек)")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("1. Сравнить методы secrets")
        print("2. Сравнить secrets.randbits и random.getrandbits")
        print("3. Сравнить secrets.randbelow и random.randint")
        print("4. Выход")

        ch = input("Выберите: ")

        if ch == "1":
            k_seq = sorted(list(map(int, input("Введите k через пробел: ").split())))
            compare_bits(k_seq)
        elif ch == "2":
            k_seq = sorted(list(map(int, input("Введите k через пробел: ").split())))
            compare_with_random_1(k_seq)
        elif ch == "3":
            k_seq = sorted(list(map(int, input("Введите k через пробел: ").split())))
            compare_with_random_2(k_seq)
        elif ch == "4":
            break
        else:
            print("Некорректный ввод!!!")


if __name__ == "__main__":
    main()