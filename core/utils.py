from pathlib import Path
import core


def get_resource_path(parts):
    return Path(core.__file__).parent.joinpath(*parts)

def byte_size(obj: int):
    return (obj.bit_length() + 7) // 8

def xor_for_bytearray(mass1: bytearray, mass2: bytearray) -> bytearray:
    arr = []
    for x, y in zip(mass1, mass2):
        arr.append(x ^ y)

    return bytearray(arr)

def factors(num):

    if type(num) != int:
        raise ValueError("Только целые числа")

    factors_list = []
    n = 2
    while num != 1:
        if num % n == 0:
            num /= n
            factors_list.append(n)

        n += 1

    return factors_list
