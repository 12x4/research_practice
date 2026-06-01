class Calculator:
    def sqrt(self, web_service):
        try:
            a = web_service.get_value()
        except ConnectionError:
            return None

        if a < 0:
            raise ValueError('Negative number')
        return a ** 0.5
