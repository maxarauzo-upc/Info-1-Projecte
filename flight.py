import os

class Flight:
    def __init__(self, id, departure_airport, arrival_airport, departure_time, arrival_time, passengers):
        self.id = id
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.passengers = int(passengers)


def PrintFlight(flight):
    # Mostra les dades d'un vol per consola
    print(
        f"ID: {flight.id} | {flight.departure_airport} ({flight.departure_time}) -> {flight.arrival_airport} ({flight.arrival_time}) | Passatgers: {flight.passengers}")


def TimeToMinutes(time):
    # Separa "HH:MM" i ho converteix a minuts des de les 00:00
    hours, minutes = map(int, time.split(':'))
    return (hours * 60) + minutes


def FlightDuration(flight):
    # Calcula la durada del vol en minuts
    dep_mins = TimeToMinutes(flight.departure_time)
    arr_mins = TimeToMinutes(flight.arrival_time)
    if arr_mins < dep_mins:
        arr_mins += 24 * 60
    return arr_mins - dep_mins


def LoadFlights(filename):
    flights = []
    if not os.path.exists(filename):
        return flights

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()

            # S'ignora la primera línia si conté les capçaleres (ID TIMD TIMA...)
            if len(parts) >= 6 and parts[0] != "ID":
                try:
                    flight_id = parts[0]  # ID (100)
                    departure_time = parts[1]  # TIMD (04:00)
                    arrival_time = parts[2]  # TIMA (07:00)
                    departure_airport = parts[3]  # DEPT (EFHK)
                    arrival_airport = parts[4]  # ARRV (LGSA)
                    passengers = int(parts[5])  # PASS (120)

                    # Creem l'objecte Flight ordenant els paràmetres com toca
                    f = Flight(flight_id, departure_airport, arrival_airport, departure_time, arrival_time, passengers)
                    flights.append(f)
                except ValueError:
                    continue
    return flights


def SaveFlights(flights, filename):
    # Guarda la llista de vols en un fitxer de text
    with open(filename, 'w') as file:
        for f in flights:
            file.write(
                f"{f.id} {f.departure_airport} {f.arrival_airport} {f.departure_time} {f.arrival_time} {f.passengers}\n")


def PrintFlights(flights):
    # Mostra tots els vols de la llista per consola
    for f in flights:
        PrintFlight(f)


def AddFlight(flights, flight):
    # Afegeix un vol a la llista
    flights.append(flight)


def RemoveFlight(flights, flight_id):
    # Elimina un vol per ID. Retorna 0 si el troba o -1 si hi ha error
    for f in flights:
        if f.id == flight_id:
            flights.remove(f)
            return 0  # Èxit
    return -1  # Error: vol no trobat

flights = LoadFlights("operations.txt")

# Secció de proves
if __name__ == "__main__":
    file_test = "operations.txt"

    # 1. Prova carregar des de fitxer
    vols = LoadFlights(file_test)
    print("--- Vols carregats ---")
    PrintFlights(vols)

    # 2. Prova afegir un vol
    AddFlight(vols, Flight("A13", "LEBL", "LEPA", "19:00", "20:00", 150))
    print("\n--- Després d'afegir A13 ---")
    PrintFlights(vols)

    # 3. Prova eliminar un vol
    res = RemoveFlight(vols, "A13")
    print(f"\n--- Després d'eliminar A13 (Codi: {res}) ---")
    PrintFlights(vols)

    # 4. Prova guardar els canvis
    SaveFlights(vols, "flights_saved.txt")