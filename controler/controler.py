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

        try:
           
            with open("mesuresTemp.json", "r") as f:
                liste_mesures = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            
            liste_mesures = []

        
        liste_mesures.append(donnees)

        
        with open("mesuresTemp.json", "w") as f:
            json.dump(liste_mesures, f, indent=4)

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
                            
                            if GPIO.input(self.platine.btn_debut_fin) == GPIO.LOW:
                                self.en_cours = self.platine.attendre_bouton_debut_fin()
                                if not self.en_cours:
                                    self.lcd.clear()
                                    self.lcd.write(0, 0, "Systeme")
                                    self.lcd.write(1, 1, "arrêté")
                                    print("Système arrêté")
                                    time.sleep(2)
                                    self.lcd.clear()
                                    self.en_cours = False
                                    break
                            
                            if self.platine.bouton_mesurer_appuye():
                                valeur_manuelle = self.platine.lire_capteur()
                                maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                mesure = Mesure(maintenant, valeur_manuelle)

                                self.lcd.clear()
                                self.lcd.write(0, 0, "Mésure")
                                self.lcd.write(1, 1, "Enregistré")
                                print(f"Mesure enregistrée : {valeur_manuelle[0]}°C")

                                self.sauvegarder_mesure(mesure)
                                time.sleep(2)

                            time.sleep(0.5)

                        
                        
                        

        except KeyboardInterrupt:
            
            self.lcd.clear()
            self.lcd.write(0, 0, "Programme")
            self.lcd.write(1, 1, "terminé")
            self.platine.cleanup()
