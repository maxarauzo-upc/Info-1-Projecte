import os


class Aircraft:
    # Constructor de la classe amb l'aeroport inicial (Step 1)
    def __init__(self, callsign, aircraft_type, capacity, initial_airport):
        self.callsign = callsign
        self.type = aircraft_type
        self.capacity = int(capacity)
        self.initial_airport = initial_airport


def PrintAircraft(aircraft):
    print(
        f"Callsign: {aircraft.callsign} | Type: {aircraft.type} | Capacity: {aircraft.capacity} | Base: {aircraft.initial_airport}")


def LoadAircrafts(filename):
    aircrafts = []
    if not os.path.exists(filename):
        return aircrafts

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            # Ignorem la capçalera i línies incompletes
            if len(parts) >= 4 and parts[0] != "CALLSIGN":
                try:
                    callsign = parts[0]
                    aircraft_type = parts[1]
                    capacity = int(parts[2])
                    initial_airport = parts[3]
                    aircrafts.append(Aircraft(callsign, aircraft_type, capacity, initial_airport))
                except ValueError:
                    continue
            # Compatibilitat amb fitxers de 3 columnes (per defecte "LEBL")
            elif len(parts) == 3 and parts[0] != "CALLSIGN":
                try:
                    aircrafts.append(Aircraft(parts[0], parts[1], int(parts[2]), "LEBL"))
                except ValueError:
                    continue
    return aircrafts


def SaveAircrafts(aircrafts, filename):
    with open(filename, 'w') as file:
        file.write("CALLSIGN AC-TYPE SEATS INITIAL_AIRPORT\n")
        for a in aircrafts:
            file.write(f"{a.callsign} {a.type} {a.capacity} {a.initial_airport}\n")


def PrintAircrafts(aircrafts):
    for a in aircrafts:
        PrintAircraft(a)


def AddAircraft(aircrafts, aircraft):
    aircrafts.append(aircraft)


def RemoveAircraft(aircrafts, callsign):
    for a in aircrafts:
        if a.callsign == callsign:
            aircrafts.remove(a)
            return 0
    return -1


# Secció de proves (Step 1)
if __name__ == "__main__":
    avions = LoadAircrafts("aircrafts.txt")
    print("--- Avions carregats (Step 1) ---")
    PrintAircrafts(avions)

    AddAircraft(avions, Aircraft("TEST1", "A320", 180, "LEBL"))
    SaveAircrafts(avions, "aircrafts_saved.txt")