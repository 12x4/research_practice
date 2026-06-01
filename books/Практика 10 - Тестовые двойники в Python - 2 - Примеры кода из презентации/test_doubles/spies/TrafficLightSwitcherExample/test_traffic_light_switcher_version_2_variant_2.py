import unittest
from test_doubles.spies.TrafficLightSwitcherExample.traffic_light_switcher import TrafficLightSwitcher


class SpyTrafficLight:
    switch_calls_order = []

    def switch(self):
        SpyTrafficLight.switch_calls_order.append(self)  # добавляем ссылку на себя


class TrafficLightSwitcherTests(unittest.TestCase):
    def setUp(self):
        SpyTrafficLight.switch_calls_order = []  # перед тестом очищаем список вызовов

    def test_switch_WhenCalledOnce_FirstSwitchesRedTrafficLightThenGreen(self):
        green = SpyTrafficLight()
        red = SpyTrafficLight()
        traffic_light_switcher = TrafficLightSwitcher(green, red)

        traffic_light_switcher.switch()

        self.assertEqual([green, red], SpyTrafficLight.switch_calls_order)

    def test_switch_WhenCalled_FirstSwitchesRedTrafficLightThenGreen(self):
        green = SpyTrafficLight()
        red = SpyTrafficLight()
        traffic_light_switcher = TrafficLightSwitcher(green, red)

        traffic_light_switcher.switch()
        traffic_light_switcher.switch()

        self.assertEqual([green, red, red, green], SpyTrafficLight.switch_calls_order)


if __name__ == '__main__':
    unittest.main()
