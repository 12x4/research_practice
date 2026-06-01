import matplotlib.pyplot as plt
import random
import time


def gcd_euclid(a, b):
    steps = 0
    while b != 0:
        a, b = b, a % b
    return a, steps


def gcd_extended(a, b):
    if b == 0:
        return a, 1, 0, 1
    else:
        d, x1, y1, steps = gcd_extended(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return d, x, y, steps + 1


def menu():
    while True:
        print("\nПРОГРАММА ДЛЯ ВЫЧИСЛЕНИЯ НОД")
        print("1. Вычислить НОД (алгоритм Евклида)")
        print("2. Вычислить НОД (расширенный алгоритм Евклида)")
        print("3. Тест НОД с генерацией длинных чисел (4 метода)")
        print("4. Сравнить производительность")
        print("5. Выход")

        choice = input("Введите ваш выбор (1-5): ")

        if choice == "1":
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            if a < 0 or b < 0:
                print("Числа должны быть неотрицательными.")
                continue
            start = time.time()
            d, steps = gcd_euclid(a, b)
            elapsed = time.time() - start
            print(f"НОД({a}, {b}) = {d}")
            print(f"Количество шагов: {steps}")
            print(f"Затраченное время: {elapsed:.6f} секунд")

        elif choice == "2":
            a = int(input("Введите первое число: "))
            b = int(input("Введите второе число: "))
            if a < 0 or b < 0:
                print("Числа должны быть неотрицательными.")
                continue
            start = time.time()
            d, x, y, steps = gcd_extended(a, b)
            elapsed = time.time() - start
            print(f"НОД({a}, {b}) = {d}")
            print(f"Коэффициенты: x={x}, y={y}")
            print(f"Количество шагов: {steps}")
            print(f"Затраченное время: {elapsed:.6f} секунд")

        elif choice == "3":
            sizes = [10, 50, 100, 200, 500, 1000]

            times_randint = []
            times_getrandbits = []
            times_odd_randint = []
            times_odd_getrandbits = []

            print("\nТестирование методов генерации на разных битностях...")

            for k in sizes:
                print(f"\nТестирование для k = {k}")

                # a.i. randint
                start_val = 2 ** (k - 1)
                end_val = 2 ** k - 1
                n1 = random.randint(start_val, end_val)
                n2 = random.randint(start_val, end_val)

                start_time = time.time()
                result, steps = gcd_euclid(n1, n2)
                elapsed = time.time() - start_time
                times_randint.append(elapsed)
                print(f"  a.i. randint: {elapsed:.6f} сек, шагов: {steps}")

                # a.ii. getrandbits
                n1 = random.getrandbits(k)
                n1 |= (1 << (k - 1))
                n2 = random.getrandbits(k)
                n2 |= (1 << (k - 1))

                start_time = time.time()
                result, steps = gcd_euclid(n1, n2)
                elapsed = time.time() - start_time
                times_getrandbits.append(elapsed)
                print(f"  a.ii. getrandbits: {elapsed:.6f} сек, шагов: {steps}")

                # б.i. нечетное randint
                n1 = random.randint(2 ** (k - 1), 2 ** k - 1)
                n1 |= 1
                n2 = random.randint(2 ** (k - 1), 2 ** k - 1)
                n2 |= 1

                start_time = time.time()
                result, steps = gcd_euclid(n1, n2)
                elapsed = time.time() - start_time
                times_odd_randint.append(elapsed)
                print(f"  б.i. нечетное randint: {elapsed:.6f} сек, шагов: {steps}")

                # б.ii. нечетное getrandbits
                n1 = random.getrandbits(k)
                n1 |= (1 << (k - 1))
                n1 |= 1
                n2 = random.getrandbits(k)
                n2 |= (1 << (k - 1))
                n2 |= 1

                start_time = time.time()
                result, steps = gcd_euclid(n1, n2)
                elapsed = time.time() - start_time
                times_odd_getrandbits.append(elapsed)
                print(f"  б.ii. нечетное getrandbits: {elapsed:.6f} сек, шагов: {steps}")

            plt.figure(figsize=(10, 6))
            plt.plot(sizes, times_randint, label="a.i. randint", linewidth=2, marker='o')
            plt.plot(sizes, times_getrandbits, label="a.ii. getrandbits", linewidth=2, marker='s')
            plt.plot(sizes, times_odd_randint, label="б.i. нечетное randint", linewidth=2, marker='^')
            plt.plot(sizes, times_odd_getrandbits, label="б.ii. нечетное getrandbits", linewidth=2, marker='d')
            plt.xlabel("Размер числа (в битах)")
            plt.ylabel("Время (секунды)")
            plt.title("Сравнение производительности генерации и GCD")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        elif choice == "4":
            sizes = [10, 50, 100, 200, 500, 1000]
            times_euclid = []
            times_extended = []

            for size in sizes:
                a = random.getrandbits(size)
                b = random.getrandbits(size)

                start = time.time()
                _, _ = gcd_euclid(a, b)
                times_euclid.append(time.time() - start)

                start = time.time()
                _, _, _, _ = gcd_extended(a, b)
                times_extended.append(time.time() - start)

                print(f"Размер {size} бит → Евклид: {times_euclid[-1]:.6f}с, Расширенный: {times_extended[-1]:.6f}с")

            plt.plot(sizes, times_euclid, label="Алгоритм Евклида")
            plt.plot(sizes, times_extended, label="Расширенный Евклид")
            plt.xlabel("Размер числа (в битах)")
            plt.ylabel("Время (секунды)")
            plt.title("Сравнение производительности алгоритмов Евклида")
            plt.legend()
            plt.grid(True)
            plt.show()

        elif choice == "5":
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    menu()