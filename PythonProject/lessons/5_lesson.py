import time
import matplotlib.pyplot as plt

# 1. Быстрое возведение в степень (без модуля)
def fast_power(base, exponent):
    result = 1
    while exponent > 0:
        if exponent & 1:
            result *= base
        base *= base
        exponent >>= 1
    return result

# 2. Быстрое возведение в степень по модулю
def modular_exponentiation(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result

tests = [
    (5, 117, 19),
    (2, 20, 17),
    (7, 256, 13),
    (123456, 654321, 123)
]

fast_times = []
modular_times = []
labels = []

for base, exponent, modulus in tests:
    start = time.time()
    fast_power(base, exponent)
    t1 = (time.time() - start) * 1e6

    start = time.time()
    modular_exponentiation(base, exponent, modulus)
    t2 = (time.time() - start) * 1e6

    fast_times.append(t1)
    modular_times.append(t2)
    labels.append(f"{base}^{exponent}%{modulus}")

for i in range(len(tests)):
    print(f"{labels[i]}: fast_power = {fast_times[i]:.2f} мкс, modular_exp = {modular_times[i]:.2f} мкс")

plt.figure(figsize=(10, 6))
plt.plot(labels, fast_times, marker='o', color='blue', label='fast_power')
plt.plot(labels, modular_times, marker='o', color='green', label='modular_exponentiation')

plt.xlabel("Тестовые данные (base^exponent % modulus)")
plt.ylabel("Время (мкс)")
plt.title("Сравнение скорости fast_power и modular_exponentiation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
