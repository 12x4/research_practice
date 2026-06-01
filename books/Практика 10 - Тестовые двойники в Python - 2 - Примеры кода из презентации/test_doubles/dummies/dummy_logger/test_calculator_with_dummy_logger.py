import unittest
from test_doubles.dummies.dummy_logger.calculator import Calculator


class CalculatorTests(unittest.TestCase):
    def test_sqrt_ReceivePositiveNumber_ReturnItsSqrt(self):
        calculator = Calculator()

        result = calculator.sqrt(4, None)  # None - dummy

        self.assertEqual(2, result)


if __name__ == '__main__':
    unittest.main()
