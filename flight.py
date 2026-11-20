class Flight:
    def __init__(self, flight_id, dep_time, arr_time, dep_airport, arr_airport, passengers):
        self.id = flight_id
        self.departure_time = dep_time
        self.arrival_time = arr_time
        self.departure_airport = dep_airport
        self.arrival_airport = arr_airport
        self.passengers = int(passengers)
        self.assigned_aircraft = None

def TimeToMinutes(time_str):
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])

def FlightDuration(flight):
    dep = TimeToMinutes(flight.departure_time)
    arr = TimeToMinutes(flight.arrival_time)
    if arr < dep:
        arr += 24 * 60
    return arr - dep

def ResetAssignments(operations):
    for f in operations:
        f.assigned_aircraft = None

def LoadFlights(filename="Operations.txt"):
    flights = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                parts = line.strip().split()
                if len(parts) >= 6:
                    flights.append(Flight(parts[0], parts[1], parts[2], parts[3], parts[4], int(parts[5])))
    except FileNotFoundError:
        pass
    return flights