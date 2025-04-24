import time
import json
from datetime import datetime
from view.platine import Platine
from model.mesure import Mesure
import RPi.GPIO as GPIO
from LCD1602 import CharLCD1602

class Controleur:
    def __init__(self):
        
        self.platine = Platine()
        self.lcd = CharLCD1602()
        self.en_cours = False  

    def sauvegarder_mesure(self, mesure: Mesure):
        
        donnees = {
            "dateHeure": mesure.dateHeureMesure,
            "valeur": mesure.dataMesure
        }
        with open("mesuresTemp.json", "a") as f:
            json.dump(donnees, f)
            f.write("\n")
        print("Mésure sauvegardée")

    def debutter_programme(self):
        try:
            while True:
                
                self.lcd.clear()
                self.lcd.write(0, 0, "Appuyez pour")
                self.lcd.write(1, 1, "demarrer...")
                
                self.en_cours = self.platine.attendre_bouton_debut_fin()

                if self.en_cours:
                    self.lcd.clear()
                    self.lcd.write(0, 0, "Systeme commencé")
                    print("Système demarré")

                    while self.en_cours:
                        
                        valeur = self.platine.lire_capteur()
 
                        self.lcd.clear()
                        self.lcd.write(0, 0, "Température (C):")
                        self.lcd.write(1, 1, str(valeur[0]))
                        
                        
                        for _ in range(10):  
                            if self.platine.bouton_mesurer_appuye():
                                self.lcd.clear()
                                self.lcd.write(0, 0, "MESURE")
                                self.lcd.write(1, 1, "MANUELLE")
                                print("Mesure manuelle")
                                time.sleep(2)  
                            time.sleep(0.5)

                        
                        if GPIO.input(self.platine.btn_debut_fin) == GPIO.LOW:
                            self.en_cours = self.platine.attendre_bouton_debut_fin()
                            if not self.en_cours:
                                self.lcd.clear()
                                self.lcd.write(0, 0, "Systeme")
                                self.lcd.write(1, 1, "arrêté")
                                print("Systeme terminé")
                                time.sleep(2)
                                self.lcd.clear()

        except KeyboardInterrupt:
            
            self.lcd.clear()
            self.lcd.write(0, 0, "Programme")
            self.lcd.write(1, 1, "terminé")
            time.sleep(2)
            self.platine.cleanup()
