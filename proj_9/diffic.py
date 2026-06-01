import logging
import os
from sympy import factorint
import secrets

from core.utils_for_rsa import *
from core.utils import *
from core.diffic import DiffHell

# Код перешел в core

def main():

    Alice = DiffHell()
    Alice.gen_pg()

    # bob получает p и g
    Bob = DiffHell(pg=Alice.get_pg())

    # Генерируют часть ключей
    Alice.gen_part_key()
    Bob.gen_part_key()

    Alice.proc_key(Bob.get_part_key())
    Bob.proc_key(Alice.get_part_key())

    print(Alice.key, Bob.key)

if __name__ == "__main__":
    main()



