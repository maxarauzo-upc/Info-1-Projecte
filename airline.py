import matplotlib.pyplot as plt
from flight import TimeToMinutes, ResetAssignments


class Airline:
    def __init__(self, name, fleet, operations, airports=None):
        self.name = name
        self.fleet = fleet
        self.operations = operations
        self.airports = airports if airports is not None else {}


def PrintAirline(airline):
    print(f"--- Aerolínia: {airline.name} ---")
    print(f"Total avions a la flota: {len(airline.fleet)}")
    print(f"Total vols programats: {len(airline.operations)}")
    print(f"Total aeroports registrats: {len(airline.airports)}")


# --- STEP 4: Algorisme A (1 vol per avió) ---
def AssignFlightsAlgorithmA(airline):
    ResetAssignments(airline.operations)
    assigned_aircrafts = set()

    for flight in airline.operations:
        for aircraft in airline.fleet:
            if aircraft.callsign not in assigned_aircrafts:
                if aircraft.capacity >= flight.passengers and aircraft.initial_airport == flight.departure_airport:
                    flight.assigned_aircraft = aircraft
                    assigned_aircrafts.add(aircraft.callsign)
                    break


# --- STEP 5: Algorisme B (Fins a 2 vols per avió) ---
def AssignFlightsAlgorithmB(airline):
    ResetAssignments(airline.operations)
    aircraft_flights = {a.callsign: [] for a in airline.fleet}

    for flight in airline.operations:
        for aircraft in airline.fleet:
            assigned = aircraft_flights[aircraft.callsign]

            # Cas 1: L'avió no té cap vol
            if len(assigned) == 0:
                if aircraft.capacity >= flight.passengers and aircraft.initial_airport == flight.departure_airport:
                    flight.assigned_aircraft = aircraft
                    assigned.append(flight)
                    break

            # Cas 2: L'avió ja té 1 vol (comprovem connexió i 2 hores de pausa)
            elif len(assigned) == 1:
                prev_flight = assigned[0]
                arr_time_prev = TimeToMinutes(prev_flight.arrival_time)
                dep_time_next = TimeToMinutes(flight.departure_time)

                if dep_time_next < arr_time_prev:
                    dep_time_next += 24 * 60

                if (aircraft.capacity >= flight.passengers and
                        prev_flight.arrival_airport == flight.departure_airport and
                        (dep_time_next - arr_time_prev) >= 120):
                    flight.assigned_aircraft = aircraft
                    assigned.append(flight)
                    break


# --- STEP 6: Ubicació dels avions al final del dia ---
def GetEndOfDayLocations(airline):
    locations = {}
    for aircraft in airline.fleet:
        assigned = [f for f in airline.operations if
                    f.assigned_aircraft and f.assigned_aircraft.callsign == aircraft.callsign]
        if len(assigned) > 0:
            assigned.sort(key=lambda x: TimeToMinutes(x.arrival_time))
            locations[aircraft.callsign] = assigned[-1].arrival_airport
        else:
            locations[aircraft.callsign] = aircraft.initial_airport
    return locations


# --- STEP 7: Gràfic Comparatiu ---
def PlotFlightsComparison(airline):
    # Guardem l'estat actual
    original_assignments = [(f, f.assigned_aircraft) for f in airline.operations]

    # Càlcul programat (tots els vols)
    sched_counts = _calculate_hourly_flights(airline.operations)

    # Càlcul Algorisme A
    AssignFlightsAlgorithmA(airline)
    assigned_a = [f for f in airline.operations if f.assigned_aircraft is not None]
    algo_a_counts = _calculate_hourly_flights(assigned_a)

    # Càlcul Algorisme B
    AssignFlightsAlgorithmB(airline)
    assigned_b = [f for f in airline.operations if f.assigned_aircraft is not None]
    algo_b_counts = _calculate_hourly_flights(assigned_b)

    # Restaurem assignacions originals
    for f, a in original_assignments:
        f.assigned_aircraft = a

    hours_labels = [f"{h:02d}:00" for h in range(24)]
    x = range(24)

    plt.figure(figsize=(14, 6))
    plt.bar([i - 0.25 for i in x], sched_counts, width=0.25, label='Programats (Tots)', color='#94A3B8')
    plt.bar(x, algo_a_counts, width=0.25, label='Algorisme A (1 vol/avió)', color='#10B981')
    plt.bar([i + 0.25 for i in x], algo_b_counts, width=0.25, label='Algorisme B (2 vols/avió)', color='#3B82F6')

    plt.xlabel('Franja Horària')
    plt.ylabel('Nombre de Vols a l\'Aire')
    plt.title(f'Comparativa d\'Assignació de Vols - {airline.name}')
    plt.xticks(x, hours_labels, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def _calculate_hourly_flights(flights_list):
    counts = [0] * 24
    for flight in flights_list:
        dep_mins = TimeToMinutes(flight.departure_time)
        arr_mins = TimeToMinutes(flight.arrival_time)
        if arr_mins < dep_mins:
            arr_mins += 24 * 60
        for hour in range(24):
            if dep_mins < (hour + 1) * 60 and arr_mins > hour * 60:
                counts[hour] += 1
    return counts


# --- STEP 7: Mapa de Rutes per Avió ---
def PlotAircraftRoutes(airline, callsign):
    assigned = [f for f in airline.operations if f.assigned_aircraft and f.assigned_aircraft.callsign == callsign]
    if not assigned:
        print(f"L'avió {callsign} no té cap vol assignat.")
        return

    plt.figure(figsize=(10, 6))
    plt.title(f"Mapa de Rutes Geolocalitzat - Avió {callsign}")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, linestyle='--', alpha=0.5)

    for f in assigned:
        dep = airline.airports.get(f.departure_airport)
        arr = airline.airports.get(f.arrival_airport)
        if dep and arr:
            plt.plot([dep.longitude, arr.longitude], [dep.latitude, arr.latitude], 'ro-', linewidth=2, markersize=8)
            plt.text(dep.longitude + 0.2, dep.latitude + 0.2, f"{dep.code} ({f.departure_time})", fontsize=9,
                     fontweight='bold')
            plt.text(arr.longitude + 0.2, arr.latitude + 0.2, f"{arr.code} ({f.arrival_time})", fontsize=9,
                     fontweight='bold')

    plt.tight_layout()
    plt.show()

# Secció de proves (Step 4, 5, 6, 7)
if __name__ == "__main__":
    from aircraft import LoadAircrafts
    from flight import LoadFlights
    from airport import LoadAirports

    ac = LoadAircrafts("aircrafts.txt")
    fl = LoadFlights("operations.txt")
    ap = LoadAirports("airports.txt")

    airline = Airline("Vueling", ac, fl, ap)
    PrintAirline(airline)

    AssignFlightsAlgorithmB(airline)
    PlotFlightsComparison(airline)