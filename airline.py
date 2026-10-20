import matplotlib.pyplot as plt
from flight import TimeToMinutes


def PlotFlights(airline):
    # Inicialitzem un comptador de vols per a cada hora (0 a 23)
    flights_per_hour = [0] * 24

    for flight in airline.operations:
        dep_mins = TimeToMinutes(flight.departure_time)
        arr_mins = TimeToMinutes(flight.arrival_time)

        # Ajust per si el vol arriba l'endemà
        if arr_mins < dep_mins:
            arr_mins += 24 * 60

        # Comprovem per a cada franja d'1 hora si el vol està a l'aire
        for hour in range(24):
            hour_start = hour * 60
            hour_end = (hour + 1) * 60

            # Un vol està a l'aire durant aquesta hora si s'encavalquen els intervals
            if dep_mins < hour_end and arr_mins > hour_start:
                flights_per_hour[hour] += 1

    # Etiquetes per a l'eix X (format 00:00, 01:00, ..., 23:00)
    hours_labels = [f"{h:02d}:00" for h in range(24)]

    # Creació del gràfic de barres
    plt.figure(figsize=(12, 6))
    plt.bar(hours_labels, flights_per_hour, color='skyblue', edgecolor='blue')
    plt.xlabel('Franja Horària')
    plt.ylabel('Nombre de Vols a l\'Aire')
    plt.title(f'Vols a l\'Aire per Hora - {airline.name}')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

class Airline:
    # Constructor amb els atributs de l'aerolínia
    def __init__(self, name, fleet, operations):
        self.name = name  # Nom de l'aerolínia (text)
        self.fleet = fleet  # Flota (llista d'objectes Aircraft)
        self.operations = operations  # Operacions (llista d'objectes Flight)


def PrintAirline(airline):
    # Mostra les dades de l'aerolínia per consola
    print(f"--- Aerolínia: {airline.name} ---")
    print(f"Total avions a la flota: {len(airline.fleet)}")
    print(f"Total vols programats: {len(airline.operations)}")


# Secció de proves
if __name__ == "__main__":
    from aircraft import LoadAircrafts
    from flight import LoadFlights

    # Carreguem dades dels fitxers
    aircrafts = LoadAircrafts("aircrafts.txt")
    flights = LoadFlights("Operations.txt")

    # Creem l'aerolínia i mostrem les dades
    airline = Airline("Vueling", aircrafts, flights)
    PrintAirline(airline)

    # Generem el gràfic de vols a l'aire
    PlotFlights(airline)