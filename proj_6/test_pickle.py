import unittest
from core.pickle1337 import Pickle1337

import os
import tempfile


class TestPickle(unittest.TestCase):

    def test_int_dump_1(self):
        number = 125
        result = b"I\x01}"

        self.assertEqual(result, Pickle1337.dump(number))

    def test_int_load_1(self):
        data = b"I\x01}"
        result = 125

        self.assertEqual(result, Pickle1337.load(data))

    def test_int_dump_2(self):
        number = 0
        result = b"I\x01\x00"

        self.assertEqual(result, Pickle1337.dump(number))

    def test_int_load_2(self):
        data = b"I\x01\x00"
        result = 0

        self.assertEqual(result, Pickle1337.load(data))

    def test_int_dump_3(self):
        number = -8
        result = b"I\x80\x08"

        self.assertEqual(result, Pickle1337.dump(number))

    def test_int_load_3(self):
        data = b"I\x80\x08"
        result = -8

        self.assertEqual(result, Pickle1337.load(data))

    def test_big_positive_int(self):
        number = 256 ** 127 - 1
        dumped = Pickle1337.dump(number)

        self.assertEqual(number, Pickle1337.load(dumped))

    def test_big_negative_int(self):
        number = 256 ** 128 * -1 + 1
        dumped = Pickle1337.dump(number)

        self.assertEqual(number, Pickle1337.load(dumped))

    def test_too_big_int(self):
        number = 2 ** 2000

        with self.assertRaises(Exception) as context:
            Pickle1337.dump(number)

        self.assertEqual("Слишком большое число, макс 258 ** 127 - 1 байт", str(context.exception))

    def test_str_dump(self):
        text = "hello"
        result = b"S\x00\x00\x00\x05hello"

        self.assertEqual(result, Pickle1337.dump(text))

    def test_str_load(self):
        data = b"S\x00\x00\x00\x05hello"

        self.assertEqual("hello", Pickle1337.load(data))

    def test_empty_str_dump(self):
        text = ""
        result = b"S\x00\x00\x00\x00"

        self.assertEqual(result, Pickle1337.dump(text))

    def test_empty_str_load(self):
        data = b"S\x00\x00\x00\x00"

        # Из-за бага в load() вернётся список
        self.assertEqual("", Pickle1337.load(data))

    def test_unicode_string(self):
        text = "Привет"

        dumped = Pickle1337.dump(text)
        loaded = Pickle1337.load(dumped)

        self.assertEqual(text, loaded)

    def test_bytearray_dump(self):
        data = bytearray(b"abc")
        result = b"B\x00\x00\x00\x03abc"

        self.assertEqual(result, Pickle1337.dump(data))

    def test_bytearray_load(self):
        data = b"B\x00\x00\x00\x03abc"

        self.assertEqual(bytearray(b"abc"), Pickle1337.load(data))

    def test_empty_bytearray(self):
        data = bytearray()

        dumped = Pickle1337.dump(data)
        loaded = Pickle1337.load(dumped)

        self.assertEqual(bytearray(), loaded)

    def test_list_dump(self):
        data = [1, "abc"]

        dumped = Pickle1337.dump(data)

        expected = (
            b"U"
            + b"\x00\x00\x00\x00\x00\x0b"
            + b"I\x01\x01"
            + b"S\x00\x00\x00\x03abc"
        )

        self.assertEqual(expected, dumped)

    def test_list_load(self):
        data = [1, "abc"]

        dumped = Pickle1337.dump(data)

        self.assertEqual(data, Pickle1337.load(dumped))

    def test_empty_list(self):
        dumped = b"U\x00\x00\x00\x00\x00\x00"

        self.assertEqual([], Pickle1337.load(dumped))

    def test_list_with_invalid_type(self):
        data = [1, {"a": 1}]

        with self.assertRaises(Exception) as context:
            Pickle1337.dump(data)

        self.assertEqual("Пу-пу-пу", str(context.exception))

    def test_file_dump_and_load(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"hello world")
            temp.flush()

            file_name = temp.name

        try:
            with open(file_name, "rb") as f:
                dumped = Pickle1337.dump(f)

            loaded_file = Pickle1337.load(dumped)

            loaded_file.seek(0)
            content = loaded_file.read()

            self.assertEqual(b"hello world", content)

            loaded_file.close()

        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

    def test_text_file_dump(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
            temp.write("hello")
            temp.flush()

            file_name = temp.name

        try:
            with open(file_name, "r") as f:
                dumped = Pickle1337.dump(f)

            self.assertTrue(dumped.startswith(b"F"))

        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

if __name__ == "__main__":
    unittest.main()