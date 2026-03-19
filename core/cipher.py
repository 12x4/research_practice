import math
import random
import secrets

# from utils_for_rsa import *
# from rsa import RSA


class cipher:

    def __init__(self, rsa_key):
        self.key = rsa_key

    # Шифровка
    def encrypt(self, plaintext):

        encrypted_text = ""

        for char in plaintext.lower():
            encrypted_text += str(self.key.public_key.mod_pow(ord(char))) + " "

        return encrypted_text

    # Расшифровка
    def decrypt(self, ciphertext):
        decrypted_text = ""

        for char in ciphertext.split(" "):
            if char != "":
                decrypted_text += chr(self.key.private_key.mod_pow(int(char)))

        return decrypted_text










