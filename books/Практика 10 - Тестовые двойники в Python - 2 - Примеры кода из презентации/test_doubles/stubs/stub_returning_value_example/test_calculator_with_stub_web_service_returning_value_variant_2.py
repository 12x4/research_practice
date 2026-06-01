import unittest
from test_doubles.stubs.stub_returning_value_example.calculator import Calculator


class StubWebService:
    def __init__(self, value_to_return):
        self.value_to_return = value_to_return

    def get_value(self):
        return self.value_to_return


class CalculatorTests(unittest.TestCase):
    def test_sqrt_ReceivePositiveNumberFromWebService_ReturnNumberSqrt(self):
        stub_web_service = StubWebService(4)
        calculator = Calculator()

        result = calculator.sqrt(stub_web_service)

        self.assertEqual(2, result)

    def test_sqrt_ReceiveNegativeNumberFromWebService_RaisesException(self):
        stub_web_service = StubWebService(-1)
        calculator = Calculator()

        self.assertRaisesRegex(ValueError, 'Negative number', calculator.sqrt, stub_web_service)


if __name__ == '__main__':
    unittest.main()
