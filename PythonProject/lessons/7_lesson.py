import matplotlib.pyplot as plt
import secrets
import random
import time

def g_rb(k):
    n = secrets.randbits(k)
    n |= (1 << (k - 1))
    return n

def g_bl(k):
    n = secrets.randbelow(2 ** k - 2 ** (k - 1)) + 2 ** (k - 1)
    return n

def g_tb(k):
    n = int.from_bytes(secrets.token_bytes((k + 7) // 8), 'big')
    n &= (1 << k) - 1
    n |= (1 << (k - 1))
    return n

def r_rb(k):
    n = random.getrandbits(k)
    n |= (1 << (k - 1))
    return n

def r_ri(k):
    n = random.randint(2 ** (k - 1), 2 ** k - 1)
    return n

def cmp_secrets(k_seq):
    t1, t2, t3 = [], [], []
    for k in k_seq:
        s = time.time()
        for _ in range(100):
            g_rb(k)
        t1.append((time.time() - s) / 100)

        s = time.time()
        for _ in range(100):
            g_bl(k)
        t2.append((time.time() - s) / 100)

        s = time.time()
        for _ in range(100):
            g_tb(k)
        t3.append((time.time() - s) / 100)

    plt.figure(figsize=(8, 5))
    plt.plot(list(k_seq), t1, color='orange', label='secrets.randbits')
    plt.plot(list(k_seq), t2, color='red', label='secrets.randbelow')
    plt.plot(list(k_seq), t3, color='purple', label='secrets.token_bytes')
    plt.xlabel('k (биты)')
    plt.ylabel('t (с)')
    plt.title('secrets.randbits, secrets.randbelow, secrets.token_bytes')
    plt.legend()
    plt.show()

def cmp_rb(k_seq):
    t1, t2 = [], []
    for k in k_seq:
        s = time.time()
        for _ in range(100):
            g_rb(k)
        t1.append((time.time() - s) / 100)

        s = time.time()
        for _ in range(100):
            r_rb(k)
        t2.append((time.time() - s) / 100)

    plt.figure(figsize=(8, 5))
    plt.plot(list(k_seq), t1, color='red', label='secrets.randbits')
    plt.plot(list(k_seq), t2, color='orange', label='random.getrandbits')
    plt.xlabel('k (биты)')
    plt.ylabel('t (c)')
    plt.title('secrets.randbits и random.getrandbits')
    plt.legend()
    plt.show()

def cmp_bl(k_seq):
    t1, t2 = [], []
    for k in k_seq:
        s = time.time()
        for _ in range(100):
            g_bl(k)
        t1.append((time.time() - s) / 100)

        s = time.time()
        for _ in range(100):
            r_ri(k)
        t2.append((time.time() - s) / 100)

    plt.figure(figsize=(8, 5))
    plt.plot(list(k_seq), t1, color='purple', label='secrets.randbelow')
    plt.plot(list(k_seq), t2, color='red', label='random.randint')
    plt.xlabel('k (биты)')
    plt.ylabel('t (с)')
    plt.title('secrets.randbelow и random.randint')
    plt.legend()
    plt.show()


def menu():
    while True:
        print("1. Протестировать генерацию")
        print("2. Сравнить secrets методы")
        print("3. Сравнить randbits")
        print("4. Сравнить randbelow/randint")
        print("5. Выход")

        choice = input(">>> ")

        if choice == "1":
            k = int(input("k: "))

            print(f"\nЧисла битности {k}:")
            print(f"randbits:    {g_rb(k)}")
            print(f"randbelow:   {g_bl(k)}")
            print(f"token_bytes: {g_tb(k)}")

        elif choice == "2":
            print("\n1. Диапазон OR 2. Список (числа через запятую)")
            c = input(">>> ")

            if c == "1":
                start = int(input("Начало: "))
                end = int(input("Конец: "))
                step = int(input("Шаг: "))
                k_seq = range(start, end, step)
            else:
                vals = input("Значения: ")
                k_seq = [int(x.strip()) for x in vals.split(',')]

            cmp_secrets(k_seq)

        elif choice == "3":
            print("\n1. Диапазон OR 2. Список (числа через запятую)")
            c = input(">>> ")

            if c == "1":
                start = int(input("Начало: "))
                end = int(input("Конец: "))
                step = int(input("Шаг: "))
                k_seq = range(start, end, step)
            else:
                vals = input("Значения: ")
                k_seq = [int(x.strip()) for x in vals.split(',')]

            cmp_rb(k_seq)

        elif choice == "4":
            print("\n1. Диапазон OR 2. Список (числа через запятую)")
            c = input(">>> ")

            if c == "1":
                start = int(input("Начало: "))
                end = int(input("Конец: "))
                step = int(input("Шаг: "))
                k_seq = range(start, end, step)
            else:
                vals = input("Значения: ")
                k_seq = [int(x.strip()) for x in vals.split(',')]

            cmp_bl(k_seq)

        elif choice == "5":
            break

        else:
            print("Ошибка")


if __name__ == "__main__":
    menu()