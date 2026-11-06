import os

class Flight:
    def __init__(self, id, departure_airport, arrival_airport, departure_time, arrival_time, passengers):
        self.id = id
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.passengers = int(passengers)
        self.assigned_aircraft = None  # Step 3: Avió assignat (None per defecte)

def PrintFlight(flight):
    assigned = flight.assigned_aircraft.callsign if flight.assigned_aircraft else "NO ASSIGNAT"
    print(f"ID: {flight.id} | {flight.departure_airport} ({flight.departure_time}) -> {flight.arrival_airport} ({flight.arrival_time}) | Pax: {flight.passengers} | Avió: {assigned}")

def TimeToMinutes(time):
    hours, minutes = map(int, time.split(':'))
    return (hours * 60) + minutes

def FlightDuration(flight):
    dep_mins = TimeToMinutes(flight.departure_time)
    arr_mins = TimeToMinutes(flight.arrival_time)
    if arr_mins < dep_mins:
        arr_mins += 24 * 60
    return arr_mins - dep_mins

def ResetAssignments(flights):
    # Restableix tots els vols a sense assignar
    for f in flights:
        f.assigned_aircraft = None

def LoadFlights(filename):
    flights = []
    if not os.path.exists(filename):
        return flights

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 6 and parts[0] != "ID":
                try:
                    # Detecta si el format és ID TIMD TIMA DEPT ARRV PASS
                    if ':' in parts[1]:
                        f = Flight(parts[0], parts[3], parts[4], parts[1], parts[2], parts[5])
                    else:
                        f = Flight(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
                    flights.append(f)
                except ValueError:
                    continue
    return flights

def SaveFlights(flights, filename):
    with open(filename, 'w') as file:
        for f in flights:
            file.write(f"{f.id} {f.departure_time} {f.arrival_time} {f.departure_airport} {f.arrival_airport} {f.passengers}\n")

def PrintFlights(flights):
    for f in flights:
        PrintFlight(f)

def AddFlight(flights, flight):
    flights.append(flight)

def RemoveFlight(flights, flight_id):
    for f in flights:
        if f.id == flight_id:
            flights.remove(f)
            return 0
    return -1

# Secció de proves
if __name__ == "__main__":
    vols = LoadFlights("operations.txt")
    print("--- Vols Carregats (Step 3) ---")
    PrintFlights(vols)