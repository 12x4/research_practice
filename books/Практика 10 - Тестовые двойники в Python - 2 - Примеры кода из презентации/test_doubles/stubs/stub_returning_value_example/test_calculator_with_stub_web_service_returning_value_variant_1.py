import unittest

from test_doubles.stubs.stub_returning_value_example.calculator import Calculator


class StubWebService:
    def get_value(self):
        return 4


class CalculatorTests(unittest.TestCase):
    def test_sqrt_ReceiveNumberFromWebService_ReturnNumberSqrt(self):
        stub_web_service = StubWebService()
        calculator = Calculator()

        result = calculator.sqrt(stub_web_service)

        self.assertEqual(2, result)


if __name__ == '__main__':
    unittest.main()
