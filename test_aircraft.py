# Importem tot des de scrip aircraft.py
from aircraft import * # el * es perque importi totes les classes y funcions de l'arxiu

# Creo una instancia de la clase Aircraft amb dades de proba
aircraft = Aircraft("AAAA", "A220-100", 135)

# 'truquem' a la funció perque fagi la seva feina
PrintAircraft(aircraft)