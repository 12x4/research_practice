
a = int(input("a:"))
p = int(input("p:"))

for i in range(1, p + 1):

    if a ** i % p == 1:
        print(i)
        break











