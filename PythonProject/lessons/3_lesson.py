import random

print("Введите k:")
k = int(input())

start = 2 ** (k - 1)
end = 2 ** k - 1
n1 = random.randint(start, end)
print(f"\na.i. randint: {n1}")
print(f"Битовая длина: {n1.bit_length()}")
print(f"Двоичное представление: {bin(n1)[2:]}")
if n1 % 2 == 0:
    print("Число четное")
else:
    print("Число нечетное")

n2 = random.getrandbits(k)
n2 |= (1 << (k - 1))
print(f"\na.ii. getrandbits: {n2}")
print(f"Битовая длина: {n2.bit_length()}")
print(f"Двоичное пр едставление: {bin(n2)[2:]}")
if n2 % 2 == 0:
    print("Число четное")
else:
    print("Число нечетное")

n3 = random.randint(2 ** (k - 1), 2 ** k - 1)
n3 |= 1
print(f"\nб.i. нечетное randint: {n3}")
print(f"Битовая длина: {n3.bit_length()}")
print(f"Двоичное представление: {bin(n3)[2:]}")
if n3 % 2 == 0:
    print("Число четное")
else:
    print("Число нечетное")

n4 = random.getrandbits(k)
n4 |= (1 << (k - 1))
n4 |= 1
print(f"\nб.ii. нечетное getrandbits: {n4}")
print(f"Битовая длина: {n4.bit_length()}")
print(f"Двоичное представление: {bin(n4)[2:]}")
if n4 % 2 == 0:
    print("Число четное")
else:
    print("Число нечетное")