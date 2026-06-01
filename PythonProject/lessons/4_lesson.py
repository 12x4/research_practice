import time
import matplotlib.pyplot as plt

def fast_power(base, exponent):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        base *= base
        exponent //= 2
    return result


def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus
    return result


base = int(input("Enter base: "))
exponent = int(input("Enter exponent: "))
modulus = int(input("Enter modulus: "))

res1 = fast_power(base, exponent) % 14
print(f"fast_power {base}, {exponent} % 14 = {res1}")

res2 = modular_exponentiation(base, exponent, modulus)
print(f"modular_exponentiation {base}, {exponent}, {modulus} = {res2}")


start_time = time.perf_counter()
for _ in range(100000):
    fast_power(base, exponent)
end_time = time.perf_counter()
time_fast = end_time - start_time
print(f"Time fast_power: {time_fast} S")

start_time = time.perf_counter()
for _ in range(100000):
    modular_exponentiation(base, exponent, modulus)
end_time = time.perf_counter()
time_modular = end_time - start_time
print(f"Time modular_exponentiation: {time_modular} S")

functions = ['fast_power', 'modular_exponentiation']
times = [time_fast, time_modular]

plt.bar(functions, times, color=['red', 'blue'])
plt.xlabel('Functions')
plt.ylabel('Time (ms)')
plt.title('Time clocking')

for i, (func, t) in enumerate(zip(functions, times)):
    plt.text(i, t, f'{t} S', ha='center', va='bottom')

plt.tight_layout()
plt.show()