import unittest

from test_doubles.stubs.stub_raising_exception.calculator import Calculator


class StubWebService:
    def __init__(self, value_to_return=None, exception=None):
        self.value_to_return = value_to_return
        self.exception = exception

    def get_value(self):
        if self.exception:
            raise self.exception
        return self.value_to_return


class CalculatorTests(unittest.TestCase):
    def test_sqrt_WebServiceRaisesException_ReturnNone(self):
        stub_web_service = StubWebService(exception=ConnectionError())

        calculator = Calculator()

        result = calculator.sqrt(stub_web_service)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
