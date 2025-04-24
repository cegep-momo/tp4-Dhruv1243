import unittest
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from view.platine import Platine

Device.pin_factory = MockFactory()

class TestPlatine(unittest.TestCase):
    def setUp(self):
        self.platine = Platine(btn_debut_fin=16, btn_mesurer=26, test=True)

    def tearDown(self):
        self.platine.pin_mesure_device.close()
        self.platine.pin_demarrage_device.close()

    def test_bouton_mesure_appuye(self):
        self.platine.pin_mesure_device.pin.drive_low()
        self.assertTrue(self.platine.pin_mesure_device.is_active)  

    def test_bouton_mesure_pas_appuye(self):
        self.platine.pin_mesure_device.pin.drive_high()
        self.assertFalse(self.platine.pin_mesure_device.is_active)

if __name__ == '__main__':
    unittest.main()
