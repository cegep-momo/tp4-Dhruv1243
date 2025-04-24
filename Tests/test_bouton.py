import unittest
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from view.platine import Platine

Device.pin_factory = MockFactory()

class TestPlatine(unittest.TestCase):
    def setUp(self):
        self.platine = Platine(pin_demarrage=16, pin_mesure=26, mode_test=True)

    def test_bouton_mesure_appuye(self):
        self.platine.pin_mesure_device.pin.drive_low()
        self.assertTrue(self.platine.bouton_mesurer_appuye())

    def test_bouton_mesure_pas_appuye(self):
        self.platine.pin_mesure_device.pin.drive_high()
        self.assertFalse(self.platine.bouton_mesurer_appuye())

if __name__ == '__main__':
    unittest.main()
