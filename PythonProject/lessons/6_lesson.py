import time
import matplotlib.pyplot as plt
import random


def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_prime(bit_length):
    while True:
        num = random.getrandbits(bit_length)
        num |= 1
        if is_prime(num):
            return num


def diffie_hellman(p, g):
    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    A = pow(g, a, p)
    B = pow(g, b, p)
    key1 = pow(B, a, p)
    key2 = pow(A, b, p)
    return key1, key2


def measure_time():
    times = []
    bit_lengths = [16, 20, 24, 28, 32]

    for bits in bit_lengths:
        p = generate_prime(bits)
        g = random.randint(2, p - 2)

        start_time = time.time()
        key1, key2 = diffie_hellman(p, g)
        end_time = time.time()

        elapsed = end_time - start_time
        times.append(elapsed)

        print(f"{bits} бит: {elapsed:.6f} сек | Совпадение ключей: {key1 == key2}")

    return bit_lengths, times


def plot_results(bit_lengths, times):
    plt.figure(figsize=(10, 6))
    plt.plot(bit_lengths, times, marker='o', linestyle='-', color='blue')
    plt.xlabel('Длина простого числа (бит)')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Зависимость времени работы Diffie-Hellman от размера p')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    bit_lengths, times = measure_time()
    plot_results(bit_lengths, times)
