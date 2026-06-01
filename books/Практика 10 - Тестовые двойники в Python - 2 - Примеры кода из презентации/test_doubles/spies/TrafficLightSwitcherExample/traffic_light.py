class TrafficLight:  # Реальный класс светофора
    def __init__(self, color):  # color - может быть двух цветов: красный и зелёный
        self.color = color

    def switch(self):  # переключаем светофор, меняя цвет
        if self.color == 'red':
            self.color = 'green'
        else:
            self.color = 'red'
