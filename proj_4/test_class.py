import unittest
from main import cipher_4
from core.rsa import RSA

arr_key_bits = [64]
arr_text = ["In this noncompliant code example, "]


class  TestCipher4(unittest.TestCase):

    def test_bit_count14(self):

        with self.assertRaises(Exception) as e:
            key = 14
            key = RSA(key)
            cip = cipher_4(key, 1, 1)

            text = ""

            enc_text = cip.encrypt_blocks(text)
            temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual("Слишком маленький ключ", str(e.exception))

    def test_11(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 1, 1)

            for text in arr_text:

                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_12(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 1, 2)

            for text in arr_text:

                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_21(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 2, 1)

            for text in arr_text:

                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_22(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 2, 2)

            for text in arr_text:

                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_31(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 3, 1)

            for text in arr_text:
                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_32(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 3, 2)

            for text in arr_text:
                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_41(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 4, 1)

            for text in arr_text:
                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_42(self):

        for key in arr_key_bits:
            key = RSA(key)
            cip = cipher_4(key, 4, 2)

            for text in arr_text:
                enc_text = cip.encrypt_blocks(text)
                temp_text = cip.decrypt_blocks(enc_text)

                self.assertEqual(temp_text, text)

    def test_11_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 1, 1)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

    def test_12_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 1, 2)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

    def test_21_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 2, 1)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

    def test_22_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 2, 2)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

    def test_31_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 3, 1)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

    def test_32_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 3, 2)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

    def test_41_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 4, 1)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

    def test_42_empty(self):

        key = 16
        key = RSA(key)
        cip = cipher_4(key, 4, 2)

        text = ""

        enc_text = cip.encrypt_blocks(text)
        temp_text = cip.decrypt_blocks(enc_text)

        self.assertEqual(temp_text, text)

if __name__ == "__main__":
    unittest.main()




