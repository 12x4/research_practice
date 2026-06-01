import secrets

def gcd(a, b, i=1) -> int:
    while a%b!=0:
        a, b = b, a % b
        i += 1
    return b

def phi(n) -> int:
    count = 0
    for i in range(1, n):
        if gcd(i, n) == 1:
            count += 1
    return count

print(phi(int(input("Введите число:"))))





