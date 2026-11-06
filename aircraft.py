import os

class Aircraft:
    # Constructor de la classe i guardo les dades bàsiques  ue ens demanen
    def __init__(self, callsign, aircraft_type, capacity):
        self.callsign = callsign  # Identificador (text)
        self.type = aircraft_type  # Tipus d'avió (text)
        self.capacity = capacity  # Capacitat de passatgers (enter)


def PrintAircraft(aircraft):
    # Mostra les dades d'un avió per consola amb una sola linea
    print(f"Callsign: {aircraft.callsign} | Type: {aircraft.type} | Capacity: {aircraft.capacity}")


def LoadAircrafts(filename):
    # Carrega la llista d'avions des d'un fitxer de text
    aircrafts = []
    if not os.path.exists(filename):
        return aircrafts  # Retorna llista buida si el fitxer no existeix

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            # Valida el format (dues paraules i un número)
            if len(parts) == 3:
                try:
                    callsign = parts[0]
                    aircraft_type = parts[1]
                    capacity = int(parts[2])
                    aircrafts.append(Aircraft(callsign, aircraft_type, capacity))
                except ValueError:
                    continue  # Ignora línies amb format incorrecte
    return aircrafts


def SaveAircrafts(aircrafts, filename):
    # Guarda la llista d'avions en un fitxer de text
    with open(filename, 'w') as file:
        for a in aircrafts:
            file.write(f"{a.callsign} {a.type} {a.capacity}\n")


def PrintAircrafts(aircrafts):
    # Mostra tots els avions de la llista per consola
    for a in aircrafts:
        PrintAircraft(a)


def AddAircraft(aircrafts, aircraft):
    # Afegeix un nou avió a la
    aircrafts.append(aircraft)


def RemoveAircraft(aircrafts, callsign):
    # Elimina un avió per callsign. Retorna 0 si el troba o -1 si hi ha error
    for a in aircrafts:
        if a.callsign == callsign:
            aircrafts.remove(a)
            return 0  # Èxit
    return -1  # Error: avió no trobat


# Secció de proves
if __name__ == "__main__":
    file_test = "aircrafts.txt"

    # 1. Prova carregar des de fitxer
    avions = LoadAircrafts(file_test)
    print("--- Avions carregats ---")
    PrintAircrafts(avions)

    # 2. Prova afegir un avió
    AddAircraft(avions, Aircraft("CCCC", "B737-800", 180))
    print("\n--- Després d'afegir CCCC ---")
    PrintAircrafts(avions)

    # 3. Prova eliminar un avió
    res = RemoveAircraft(avions, "CCCC")
    print(f"\n--- Després d'eliminar CCCC (Codi: {res}) ---")
    PrintAircrafts(avions)

    # 4. Prova guardar els canvis
    SaveAircrafts(avions, "aircrafts_saved.txt")