a = int(input("Введите (a) : "))
p = int(input("Введите (p) : "))

k = 1
cur = a % p

while cur != 1:
    cur = (cur * a) % p
    k += 1

print(f"поле F({p}) равен = {k}")