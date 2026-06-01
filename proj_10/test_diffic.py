import unittest

from fontTools.varLib.merger import AligningMerger

from core.diffic import DiffHell


class TestDiffHell(unittest.TestCase):

    def test_incorrect_gen_pg(self):
        Alice = DiffHell()
        Alice.gen_pg()

        self.assertEqual(32, Alice.p.bit_length())

    # Что то похожее на stub
    def test_incorrect_proc_key(self):

        Alice = DiffHell(pg=(7, 3))

        Alice.part_key = 5
        Alice.proc_key(4)

        self.assertEqual(2, Alice.key)

    def test_full_8bit(self):

        Alice = DiffHell()
        Alice.gen_pg()

        Bob = DiffHell(pg=Alice.get_pg())

        Alice.gen_part_key()
        Bob.gen_part_key()

        Alice.proc_key(Bob.get_part_key())
        Bob.proc_key(Alice.get_part_key())

        self.assertEqual(Alice.key, Bob.key)

    def test_full_16bit(self):

        Alice = DiffHell()
        Alice.gen_pg()

        Bob = DiffHell(pg=Alice.get_pg())

        Alice.gen_part_key()
        Bob.gen_part_key()

        Alice.proc_key(Bob.get_part_key())
        Bob.proc_key(Alice.get_part_key())

        self.assertEqual(Alice.key, Bob.key)

    def test_full_64bit(self):

        Alice = DiffHell()
        Alice.gen_pg()

        Bob = DiffHell(pg=Alice.get_pg())

        Alice.gen_part_key()
        Bob.gen_part_key()

        Alice.proc_key(Bob.get_part_key())
        Bob.proc_key(Alice.get_part_key())

        self.assertEqual(Alice.key, Bob.key)

    def test_full_128bit(self):

        Alice = DiffHell()
        Alice.gen_pg()

        Bob = DiffHell(pg=Alice.get_pg())

        Alice.gen_part_key()
        Bob.gen_part_key()

        Alice.proc_key(Bob.get_part_key())
        Bob.proc_key(Alice.get_part_key())

        self.assertEqual(Alice.key, Bob.key)

    def test_exception_get_part_key(self):

        Alice = DiffHell()
        with self.assertRaises(Exception) as e:
            Alice.get_part_key()

        self.assertEqual("Сначала сгенерируйте часть ключа!", str(e.exception))

    def test_exception_proc_key(self):
        Alice = DiffHell()
        with self.assertRaises(Exception) as e:
            Alice.proc_key("Попался")
        self.assertEqual("Произошла какая то ошибка, тип полученного объекта не int", str(e.exception))

    def test_exception_bit_count(self):
        with self.assertRaises(Exception) as e:
            Alice = DiffHell(bit_count=4)
        self.assertEqual("Лучше так не делать", str(e.exception))


if __name__ == "__main__":
    unittest.main()

