import random
import sys
import matplotlib.pyplot as plt
import time

sys.setrecursionlimit(10000)

def gcd(a, b, i=1):

    while a%b!=0:

        a, b = b, a % b
        i += 1

    return b, i

def info():

    print("1 Вычислить НОД с помощью алгоритма евклида")
    print("2 Вычислить НОД с помощью расширенного алгоритма евклида")
    print("3 Сравнить производительность с построением графика")
    print("4 Выход")


def gcd_ev(a, b, iter=1):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
        iter += 1
    return x, y, a, iter


def main():
    info()
    curr = input()

    while curr != "4":

        if curr == "1":
            x = int(input("Первое число"))
            y = int(input("второе число"))

            start = time.time()
            result, count = gcd(x, y)
            stop = time.time()

            print(f"НОД чисел равен {result}")
            print(f"Количество шагов {count}")
            print(f"Затраченное время {(stop - start) * pow(10, 6)}")


        elif(curr == "2"):
            x = int(input("Первое число"))
            y = int(input("второе число"))

            start = time.time()
            res_x, res_y, result, count  = gcd_ev(x, y)
            stop = time.time()

            print(f"НОД чисел равен {result}")
            print(f"Коэффициенты x={res_x} и y={res_y}")
            print(f"Количество шагов {count}")
            print(f"Затраченное время {(stop - start) * pow(10, 6)}")

        elif curr == "3":

            x_lab = [10, 50, 100, 200, 500, 1000, 2000]
            time_gcd = []
            time_gcd_ev = []

            for n in x_lab:

                x = random.randint(pow(10, n), pow(10, n + 1) - 1)
                y = random.randint(pow(10, n), pow(10, n + 1) - 1)

                start = time.time()
                result, count = gcd(x, y)
                stop = time.time()
                time_gcd_t = stop - start
                time_gcd.append(time_gcd_t)

                start = time.time()
                res_x, res_y, result, count = gcd_ev(x, y)
                stop = time.time()
                time_gcd_ev_t = stop - start
                time_gcd_ev.append(time_gcd_ev_t)

                print(f"Размер: {n} цифр - Евклид {time_gcd_t}, Расширенный:{time_gcd_ev_t}")

            plt.plot(x_lab, time_gcd)
            plt.plot(x_lab, time_gcd_ev)
            plt.xlabel("Количество цифр")
            plt.ylabel("Время")
            plt.show()


        info()
        curr = input()



    # x1 = [0, 0, 0, 3, 0, 3]
    # y1 = [5, 0, 2, 5, 2, 0]
    #
    # x2 = [6, 6, 5, 7, 6, 6]
    # y2 = [0, 5, 5, 5, 5, 0]
    #
    # x3 = [9, 9, 11]
    # y3 = [0, 5, 5]
    #
    # for i in range(len(x1)):
    #     x1[i] += 4
    #
    # for i in range(len(x2)):
    #     x2[i] += -4
    #
    # plt.plot(x1, y1)
    # plt.plot(x2, y2)
    # plt.plot(x3, y3)
    # plt.xlabel("x - axis")
    # plt.ylabel("y - axis")
    # plt.show()


if __name__ == "__main__":
    main()