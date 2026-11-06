import os

class Airport:
    def __init__(self, code, latitude, longitude):
        self.code = code
        self.latitude = float(latitude)
        self.longitude = float(longitude)

def PrintAirport(airport):
    print(f"ICAO: {airport.code} | Lat: {airport.latitude} | Lon: {airport.longitude}")

def LoadAirports(filename):
    airports = {}
    if not os.path.exists(filename):
        return airports

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 3 and parts[0] != "CODE":
                try:
                    code = parts[0]
                    lat = float(parts[1])
                    lon = float(parts[2])
                    airports[code] = Airport(code, lat, lon)
                except ValueError:
                    continue
    return airports

def SaveAirports(airports, filename):
    with open(filename, 'w') as file:
        file.write("CODE LATITUDE LONGITUDE\n")
        for code, ap in airports.items():
            file.write(f"{ap.code} {ap.latitude} {ap.longitude}\n")

def PrintAirports(airports):
    for ap in airports.values():
        PrintAirport(ap)

def AddAirport(airports, airport):
    airports[airport.code] = airport

def RemoveAirport(airports, code):
    if code in airports:
        del airports[code]
        return 0
    return -1

# Secció de proves (Step 2)
if __name__ == "__main__":
    aeroports = LoadAirports("airports.txt")
    print("--- Aeroports carregats (Step 2) ---")
    PrintAirports(aeroports)