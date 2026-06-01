class TrafficLightSwitcher:
    def __init__(self, green, red):
        self.green, self.red = green, red

    def switch(self):  # Сначала переключает зелёный светофор, затем - красный
        self.green.switch()
        self.red.switch()
        self.green, self.red = self.red, self.green
