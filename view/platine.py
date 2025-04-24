import RPi.GPIO as GPIO
import time
import math
from ADCDevice import *

class Platine:
    def __init__(self, btn_debut_fin=16, btn_mesurer=26):
        
        self.btn_debut_fin = btn_debut_fin
        self.btn_mesurer = btn_mesurer

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.btn_debut_fin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btn_mesurer, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.systeme_actif = False

        
        self.adc = ADCDevice()
        if self.adc.detectI2C(0x4b):
            self.adc = ADS7830()
        else:
            print("Aucune adresse I2C détectée pour l'ADC. Fin du programme.")
            exit(-1)

    def attendre_bouton_debut_fin(self):
        print("En attente du bouton début/fin...")
        while True:
            if GPIO.input(self.btn_debut_fin) == GPIO.LOW:
                print("Bouton début/fin appuyé.")
                time.sleep(0.3)  
                self.systeme_actif = not self.systeme_actif
                return self.systeme_actif

    def bouton_mesurer_appuye(self):
        return GPIO.input(self.btn_mesurer) == GPIO.LOW

    def lire_capteur(self):
        valeur = self.adc.analogRead(0)  
        tension = valeur / 255.0 * 3.3
        Rt = 10 * tension / (3.3 - tension)
        tempK = 1 / (1 / (273.15 + 25) + math.log(Rt / 10) / 3950.0)
        tempC = round(tempK - 273.15, 2)
        print(f"[Thermistance] Température : {tempC}°C")
        return [tempC]

    def cleanup(self):
        self.adc.close()
        GPIO.cleanup()
