class Aircraft:
    def __init__(self, callsign, ac_type, capacity, initial_airport="LEBL"):
        self.callsign = callsign
        self.type = ac_type
        self.capacity = int(capacity)
        self.initial_airport = initial_airport

def LoadAircrafts(filename="Aircrafts.txt", pos_filename=None):
    aircrafts = []
    positions = {}

    if pos_filename:
        try:
            with open(pos_filename, "r", encoding="utf-8") as pf:
                for line in pf.readlines()[1:]:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        positions[parts[0]] = parts[2]
        except FileNotFoundError:
            pass

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                parts = line.strip().split()
                if len(parts) >= 3:
                    callsign = parts[0]
                    ac_type = parts[1]
                    capacity = int(parts[2])
                    init_ap = positions.get(callsign, parts[3] if len(parts) >= 4 else "LEBL")
                    aircrafts.append(Aircraft(callsign, ac_type, capacity, init_ap))
    except FileNotFoundError:
        pass

    return aircrafts

def SaveAircrafts(aircrafts, filename="aircrafts_end_of_day.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("CALLSIGN AC-TYPE AIRP\n")
        for a in aircrafts:
            f.write(f"{a.callsign} {a.type} {a.initial_airport}\n")