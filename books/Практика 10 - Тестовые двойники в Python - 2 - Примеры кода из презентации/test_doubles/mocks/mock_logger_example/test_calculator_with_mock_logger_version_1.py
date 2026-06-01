import unittest

from test_doubles.mocks.mock_logger_example.calculator import Calculator


class MockLogger:
    is_log_called = False

    def log(self, message):
        self.is_log_called = True


class CalculatorTests(unittest.TestCase):
    def test_sqrt_ReceiveNegativeNumber_CallsLoggersLog(self):
        mock_logger = MockLogger()
        calculator = Calculator()

        calculator.sqrt(-1, mock_logger)

        self.assertTrue(mock_logger.is_log_called)


if __name__ == '__main__':
    unittest.main()
