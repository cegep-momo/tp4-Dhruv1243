import time
import json
from datetime import datetime
from view.platine import Platine
from model.mesure import Mesure
import RPi.GPIO as GPIO
import LCD1602  

class Controleur:
    def __init__(self):
        self.platine = Platine()
        self.en_cours = False
        LCD1602.init(0x27, 1)  

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

        print("Mesure sauvegardee")

    def debutter_programme(self):
        try:
            while True:
                LCD1602.clear()
                LCD1602.write(0, 0, "Appuyez bouton")
                LCD1602.write(1, 1, "pour demarrer")

                self.en_cours = self.platine.attendre_bouton_debut_fin()

                if self.en_cours:
                    LCD1602.clear()
                    LCD1602.write(0, 0, "Systeme demarre")
                    print("Systeme demarre")

                    while self.en_cours:
                        valeur = self.platine.lire_capteur()

                        LCD1602.clear()
                        LCD1602.write(0, 0, "Temp (C):")
                        LCD1602.write(1, 1, str(valeur[0]))

                        for _ in range(10):
                            # Si on appuie de nouveau pour arreter
                            if GPIO.input(self.platine.btn_debut_fin) == GPIO.LOW:
                                self.en_cours = self.platine.attendre_bouton_debut_fin()
                                if not self.en_cours:
                                    LCD1602.clear()
                                    LCD1602.write(0, 0, "Systeme")
                                    LCD1602.write(1, 1, "arrete")
                                    print("Systeme arrete")
                                    time.sleep(2)
                                    LCD1602.clear()
                                    break

                            if self.platine.bouton_mesurer_appuye():
                                valeur_manuelle = self.platine.lire_capteur()
                                maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                mesure = Mesure(maintenant, valeur_manuelle)

                                LCD1602.clear()
                                LCD1602.write(0, 0, "Mesure")
                                LCD1602.write(1, 1, "enregistree")
                                print(f"Mesure sauvée : {valeur_manuelle[0]}°C")

                                self.sauvegarder_mesure(mesure)
                                time.sleep(2)

                            time.sleep(0.5)

        except KeyboardInterrupt:
            LCD1602.clear()
            LCD1602.write(0, 0, "Programme")
            LCD1602.write(1, 1, "termine")
            self.platine.cleanup()
