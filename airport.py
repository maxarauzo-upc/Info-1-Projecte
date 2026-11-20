class Airport:
    def __init__(self, code, longitude, latitude, description=""):
        self.code = code
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.description = description

def LoadAirports(filename="Airports.txt"):
    airports = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[1:]:
                parts = line.strip().split(maxsplit=2)
                if len(parts) >= 2:
                    code = parts[0]
                    coords = parts[1].split(",")
                    lon = float(coords[0])
                    lat = float(coords[1])
                    desc = parts[2] if len(parts) == 3 else ""
                    airports[code] = Airport(code, lon, lat, desc)
    except FileNotFoundError:
        pass
    return airports