import sys
import time
import random
sys.set_int_max_str_digits(10000)
def gcd(a, b, i=1):

    if a%b==0:
        return b, i

    return gcd(b, a%b, i + 1)

# print(gcd(210, 45))
# print(gcd(77, 7))
# print(gcd(1000, 500))
# print(gcd(100, 1))
def main():
    x = random.randint(1, pow(10, 3))
    y = random.randint(1, pow(10, 3))
    start = time.time()
    result, count = gcd(x, y)
    end = time.time()
    print(f"x={x},y={y}")
    print("Result ", result)
    print("Count iteration ", count)
    print(f"time = {(end-start)*1000000} ms")
    return count

main()
