from datetime import datetime

class Mesure:
    def __init__(self, dateHeureMesure: str, dataMesure: list):
        self.dateHeureMesure = dateHeureMesure
        self.dataMesure = dataMesure
        
    def __repr__(self):
        return f"{self.dateHeureMesure} | {self.dataMesure}"
    
    def afficherMesure(self):
        msg = f"Voici la date complète : {self.dateHeureMesure}\n"
        msg += "Voici les valeurs :\n"
        for i, val in enumerate(self.dataMesure, start=1):
            msg += f"  - Valeur {i} : {val}\n"
        return msg
        