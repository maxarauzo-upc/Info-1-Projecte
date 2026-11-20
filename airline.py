import matplotlib.pyplot as plt
import numpy as np
from flight import TimeToMinutes, ResetAssignments

class Airline:
    def __init__(self, name, fleet, operations, airports=None):
        self.name = name
        self.fleet = fleet
        self.operations = operations
        self.airports = airports if airports is not None else {}

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

def AssignFlightsAlgorithmB(airline):
    ResetAssignments(airline.operations)
    aircraft_flights = {a.callsign: [] for a in airline.fleet}

    for flight in airline.operations:
        for aircraft in airline.fleet:
            assigned = aircraft_flights[aircraft.callsign]

            if len(assigned) == 0:
                if aircraft.capacity >= flight.passengers and aircraft.initial_airport == flight.departure_airport:
                    flight.assigned_aircraft = aircraft
                    assigned.append(flight)
                    break

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

def GetEndOfDayLocations(airline):
    locations = {}
    for aircraft in airline.fleet:
        assigned = [f for f in airline.operations if f.assigned_aircraft and f.assigned_aircraft.callsign == aircraft.callsign]
        if len(assigned) > 0:
            assigned.sort(key=lambda x: TimeToMinutes(x.arrival_time))
            locations[aircraft.callsign] = assigned[-1].arrival_airport
        else:
            locations[aircraft.callsign] = aircraft.initial_airport
    return locations

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

def PlotFlightsComparison(airline):
    original_assignments = [(f, f.assigned_aircraft) for f in airline.operations]

    sched_counts = _calculate_hourly_flights(airline.operations)

    AssignFlightsAlgorithmA(airline)
    algo_a_counts = _calculate_hourly_flights([f for f in airline.operations if f.assigned_aircraft])

    AssignFlightsAlgorithmB(airline)
    algo_b_counts = _calculate_hourly_flights([f for f in airline.operations if f.assigned_aircraft])

    # Restauro las asignaciones previas
    for f, a in original_assignments:
        f.assigned_aircraft = a

    hours_labels = [f"{h:02d}:00" for h in range(24)]
    x = np.arange(24)
    width = 0.26

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(15, 7), facecolor='#0B132B')
    ax.set_facecolor('#1C2541')

    rects1 = ax.bar(x - width, sched_counts, width, label='Programados Totales', color='#64748B', edgecolor='#94A3B8', zorder=3)
    rects2 = ax.bar(x, algo_a_counts, width, label='Algoritmo A (1 vuelo/avión)', color='#06D6A0', edgecolor='#34D399', zorder=3)
    rects3 = ax.bar(x + width, algo_b_counts, width, label='Algoritmo B (2 vuelos/avión)', color='#48CAE4', edgecolor='#90E0EF', zorder=3)

    for rects in (rects1, rects2, rects3):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height}', xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    ax.set_xlabel('Franja Horaria (24h)', fontsize=11, fontweight='bold', color='#48CAE4')
    ax.set_ylabel("Vuelos en el Aire", fontsize=11, fontweight='bold', color='#48CAE4')
    ax.set_title(f'COMPARATIVA DE ASIGNACIÓN - {airline.name.upper()}', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(hours_labels, rotation=45, ha='right', fontsize=9)
    ax.grid(True, axis='y', linestyle='--', alpha=0.2, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(facecolor='#0B132B', edgecolor='#48CAE4', fontsize=10)
    plt.tight_layout()
    plt.show()

def PlotAircraftRoutes(airline, callsign):
    assigned = [f for f in airline.operations if f.assigned_aircraft and f.assigned_aircraft.callsign == callsign]
    if not assigned:
        return

    assigned.sort(key=lambda x: TimeToMinutes(x.departure_time))

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 7.5), facecolor='#0B132B')
    ax.set_facecolor('#111B33')

    # Red de aeropuertos en segundo plano
    all_lons = [ap.longitude for ap in airline.airports.values()]
    all_lats = [ap.latitude for ap in airline.airports.values()]
    ax.scatter(all_lons, all_lats, color='#3A506B', s=25, alpha=0.5, zorder=1, label='Red de Aeropuertos')
    for ap in airline.airports.values():
        ax.text(ap.longitude, ap.latitude - 0.35, ap.code, color='#4A607A', fontsize=7, ha='center', zorder=1)

    colors = ['#06D6A0', '#FFD166', '#48CAE4']
    route_lons = []
    route_lats = []

    for idx, f in enumerate(assigned):
        dep = airline.airports.get(f.departure_airport)
        arr = airline.airports.get(f.arrival_airport)
        if dep and arr:
            route_lons.extend([dep.longitude, arr.longitude])
            route_lats.extend([dep.latitude, arr.latitude])
            color = colors[idx % len(colors)]

            t = np.linspace(0, 1, 100)
            mid_lon = (dep.longitude + arr.longitude) / 2
            mid_lat = (dep.latitude + arr.latitude) / 2
            dx = arr.longitude - dep.longitude
            dy = arr.latitude - dep.latitude
            ctrl_lon = mid_lon - dy * 0.12
            ctrl_lat = mid_lat + dx * 0.12

            curve_lon = (1 - t)**2 * dep.longitude + 2 * (1 - t) * t * ctrl_lon + t**2 * arr.longitude
            curve_lat = (1 - t)**2 * dep.latitude + 2 * (1 - t) * t * ctrl_lat + t**2 * arr.latitude

            ax.plot(curve_lon, curve_lat, color=color, linewidth=7, alpha=0.18, zorder=2)
            ax.plot(curve_lon, curve_lat, color=color, linewidth=2.5, zorder=3,
                    label=f"Vuelo {idx+1}: {dep.code} ➔ {arr.code} ({f.departure_time}-{f.arrival_time})")

            mid_idx = 52
            ax.annotate('', xy=(curve_lon[mid_idx], curve_lat[mid_idx]),
                        xytext=(curve_lon[mid_idx - 3], curve_lat[mid_idx - 3]),
                        arrowprops=dict(arrowstyle="->", color=color, lw=2.5), zorder=4)

            ax.scatter([dep.longitude], [dep.latitude], color='#48CAE4', s=130, edgecolors='white', linewidth=1.5, zorder=5)
            ax.scatter([arr.longitude], [arr.latitude], color=color, s=130, edgecolors='white', linewidth=1.5, zorder=5)

            ax.annotate(f"{dep.code}\nSal: {f.departure_time}",
                        xy=(dep.longitude, dep.latitude), xytext=(0, 12 if idx == 0 else -24),
                        textcoords="offset points", ha='center', fontsize=8.5, fontweight='bold', color='white',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0B132B', edgecolor='#48CAE4', alpha=0.9), zorder=6)

            ax.annotate(f"{arr.code}\nLleg: {f.arrival_time}",
                        xy=(arr.longitude, arr.latitude), xytext=(0, 12 if idx == 1 else -24),
                        textcoords="offset points", ha='center', fontsize=8.5, fontweight='bold', color='white',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0B132B', edgecolor=color, alpha=0.9), zorder=6)

    if route_lons and route_lats:
        margin_x = max(2.5, (max(route_lons) - min(route_lons)) * 0.35)
        margin_y = max(2.0, (max(route_lats) - min(route_lats)) * 0.35)
        ax.set_xlim(min(route_lons) - margin_x, max(route_lons) + margin_x)
        ax.set_ylim(min(route_lats) - margin_y, max(route_lats) + margin_y)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#3A506B')
    ax.spines['bottom'].set_color('#3A506B')

    ax.legend(facecolor='#0B132B', edgecolor='#48CAE4', fontsize=9.5, loc='upper right')
    fig.subplots_adjust(left=0.07, right=0.97, top=0.91, bottom=0.09)
    plt.show()

