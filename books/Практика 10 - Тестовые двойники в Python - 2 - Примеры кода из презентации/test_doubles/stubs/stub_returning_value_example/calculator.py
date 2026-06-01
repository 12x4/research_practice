class Calculator:
    def sqrt(self, web_service):  # вычисление квадратного корня
        a = web_service.get_value()
        if a < 0:
            raise ValueError('Negative number')
        return a ** 0.5