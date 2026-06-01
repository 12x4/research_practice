class Calculator:
    def sqrt(self, a, logger):
        if a < 0:
            logger.log('Negative number')
            return None
        return a ** 0.5