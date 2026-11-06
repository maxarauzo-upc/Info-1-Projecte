# Interface.py - AeroManager Executive Navy Dashboard V2
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Importació dels teus mòduls existents
from aircraft import LoadAircrafts, SaveAircrafts, Aircraft
from flight import LoadFlights
from airport import LoadAirports
from airline import (Airline, AssignFlightsAlgorithmA, AssignFlightsAlgorithmB,
                     GetEndOfDayLocations, PlotFlightsComparison, PlotAircraftRoutes)


class AeroManagerNavyDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("AeroManager Pro v2.0 - Operations Control Center")
        self.root.geometry("1100x750")
        self.root.minsize(1000, 680)

        # Paleta de Colors Blau Marino (Navy Executive Theme)
        self.C_BG = "#0B132B"         # Blau Marino profund de fons
        self.C_PANEL = "#1C2541"      # Blau Marino intermedi per a panells i capçalera
        self.C_CARD = "#3A506B"       # Blau de contrast per a targetes i contingut
        self.C_BLUE_ELECTRIC = "#48CAE4" # Accent primari (Blau cel/elèctric)
        self.C_GREEN = "#06D6A0"      # Algorisme A / Validacions
        self.C_AMBER = "#FFD166"      # Algorisme B / Alertes
        self.C_PURPLE = "#7209B7"     # Comparatives i rutes
        self.C_TEXT = "#FFFFFF"       # Text blanc pur
        self.C_MUTED = "#8D99AE"      # Text secundari gris-blau

        self.root.configure(bg=self.C_BG)
        self.airline = None
        self.airports = {}

        self._configure_styles()
        self._build_header()
        self._build_workflow_bar()
        self._build_kpi_cards()
        self._build_main_content()
        self._build_footer()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Personalització de Notebook (Pestanyes)
        self.style.configure("TNotebook", background=self.C_BG, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.C_PANEL, foreground=self.C_MUTED,
                             padding=[18, 8], font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("TNotebook.Tab",
                       background=[("selected", self.C_BLUE_ELECTRIC)],
                       foreground=[("selected", "#0B132B")])

        # Personalització de Treeview (Taules)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                             background="#2B2D42", foreground="#FFFFFF", relief="flat")
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=28,
                             background=self.C_PANEL, foreground=self.C_TEXT,
                             fieldbackground=self.C_PANEL, borderwidth=0)
        self.style.map("Treeview", background=[("selected", self.C_BLUE_ELECTRIC)], foreground=[("selected", "#0B132B")])

    def _build_header(self):
        header = tk.Frame(self.root, bg=self.C_PANEL, height=75)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Logotip EETAC
        logo_loaded = False
        for ext in [".png", ".jpg", ".jpeg"]:
            logo_path = f"logo{ext}"
            if os.path.exists(logo_path):
                try:
                    img = Image.open(logo_path)
                    img = img.resize((150, 50), Image.Resampling.LANCZOS)
                    self.logo_img = ImageTk.PhotoImage(img)
                    lbl_logo = tk.Label(header, image=self.logo_img, bg=self.C_PANEL)
                    lbl_logo.pack(side="left", padx=20, pady=10)
                    logo_loaded = True
                    break
                except Exception:
                    pass

        if not logo_loaded:
            lbl_logo_fallback = tk.Label(header, text="EETAC", font=("Segoe UI", 18, "bold"),
                                         fg=self.C_BLUE_ELECTRIC, bg=self.C_PANEL)
            lbl_logo_fallback.pack(side="left", padx=25)

        # Títol principal
        lbl_title = tk.Label(header, text="AEROMANAGER PRO", font=("Segoe UI", 18, "bold"),
                             fg=self.C_TEXT, bg=self.C_PANEL)
        lbl_title.pack(side="left", padx=10)

        lbl_sub = tk.Label(header, text="• Mission Control V2", font=("Segoe UI", 11, "italic"),
                            fg=self.C_BLUE_ELECTRIC, bg=self.C_PANEL)
        lbl_sub.pack(side="left")

    def _build_workflow_bar(self):
        # Barra d'accions pas a pas
        bar = tk.Frame(self.root, bg=self.C_BG, pady=10)
        bar.pack(fill="x", padx=20)

        lbl_guide = tk.Label(bar, text="FLUX DE TREBALL:", font=("Segoe UI", 9, "bold"),
                             fg=self.C_MUTED, bg=self.C_BG)
        lbl_guide.pack(side="left", padx=(0, 10))

        # Botó PAS 1
        btn_1 = tk.Button(bar, text="1. 📁 Carregar Dades", font=("Segoe UI", 9, "bold"),
                          bg=self.C_BLUE_ELECTRIC, fg="#0B132B", activebackground="#00B4D8",
                          relief="flat", padx=12, pady=6, cursor="hand2", command=self.load_data)
        btn_1.pack(side="left", padx=4)

        # Botó PAS 2
        btn_2 = tk.Button(bar, text="2. ⚡ Algorisme A (1 Vol)", font=("Segoe UI", 9, "bold"),
                          bg=self.C_GREEN, fg="#0B132B", activebackground="#05B386",
                          relief="flat", padx=12, pady=6, cursor="hand2", command=self.run_algo_a)
        btn_2.pack(side="left", padx=4)

        # Botó PAS 3
        btn_3 = tk.Button(bar, text="3. ⚡ Algorisme B (2 Vols)", font=("Segoe UI", 9, "bold"),
                          bg=self.C_AMBER, fg="#0B132B", activebackground="#E0A96D",
                          relief="flat", padx=12, pady=6, cursor="hand2", command=self.run_algo_b)
        btn_3.pack(side="left", padx=4)

        # Botó PAS 4
        btn_4 = tk.Button(bar, text="4. 📊 Comparativa", font=("Segoe UI", 9, "bold"),
                          bg=self.C_PURPLE, fg="white", activebackground="#5C069C",
                          relief="flat", padx=12, pady=6, cursor="hand2", command=self.show_comparison)
        btn_4.pack(side="left", padx=4)

    def _build_kpi_cards(self):
        # Targetes d'indicadors
        kpi_frame = tk.Frame(self.root, bg=self.C_BG)
        kpi_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.card_fleet = self._create_card(kpi_frame, "FLOTA D'AVIONS", "0", self.C_BLUE_ELECTRIC)
        self.card_fleet.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.card_flights = self._create_card(kpi_frame, "VOLS TOTALS", "0", self.C_MUTED)
        self.card_flights.pack(side="left", fill="x", expand=True, padx=5)

        self.card_assigned = self._create_card(kpi_frame, "VOLS ASSIGNATS", "0 / 0", self.C_GREEN)
        self.card_assigned.pack(side="left", fill="x", expand=True, padx=5)

        self.card_airports = self._create_card(kpi_frame, "AEROPORTS BASE", "0", self.C_PURPLE)
        self.card_airports.pack(side="left", fill="x", expand=True, padx=(5, 0))

    def _create_card(self, parent, title, value, accent_color):
        card = tk.Frame(parent, bg=self.C_CARD, bd=0, highlightthickness=1, highlightbackground=accent_color)
        lbl_t = tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), fg=self.C_MUTED, bg=self.C_CARD)
        lbl_t.pack(anchor="w", padx=10, pady=(8, 0))
        lbl_v = tk.Label(card, text=value, font=("Segoe UI", 14, "bold"), fg=self.C_TEXT, bg=self.C_CARD)
        lbl_v.pack(anchor="w", padx=10, pady=(0, 8))
        card.value_label = lbl_v
        return card

    def _build_main_content(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # --- Pestanya 1: Flota ---
        f_ac = tk.Frame(notebook, bg=self.C_PANEL)
        notebook.add(f_ac, text=" ✈️ Flota d'Avions ")
        self.tree_ac = ttk.Treeview(f_ac, columns=("Callsign", "Type", "Capacity", "Base"), show="headings")
        for c in ("Callsign", "Type", "Capacity", "Base"):
            self.tree_ac.heading(c, text=c)
            self.tree_ac.column(c, anchor="center")
        sc_ac = ttk.Scrollbar(f_ac, orient="vertical", command=self.tree_ac.yview)
        self.tree_ac.configure(yscroll=sc_ac.set)
        self.tree_ac.pack(side="left", fill="both", expand=True)
        sc_ac.pack(side="right", fill="y")

        # --- Pestanya 2: Vols ---
        f_fl = tk.Frame(notebook, bg=self.C_PANEL)
        notebook.add(f_fl, text=" 🛫 Operacions i Assignacions ")

        filter_bar = tk.Frame(f_fl, bg=self.C_CARD, pady=5)
        filter_bar.pack(fill="x")
        tk.Label(filter_bar, text=" Filtrar per Estat:", bg=self.C_CARD, fg=self.C_TEXT, font=("Segoe UI", 9, "bold")).pack(side="left", padx=10)
        self.combo_filter = ttk.Combobox(filter_bar, values=["Tots els Vols", "Només Assignats", "Només NO Assignats"], state="readonly", width=22)
        self.combo_filter.current(0)
        self.combo_filter.pack(side="left")
        self.combo_filter.bind("<<ComboboxSelected>>", lambda e: self.update_tables())

        self.tree_fl = ttk.Treeview(f_fl, columns=("ID", "Origin", "Dest", "DepTime", "ArrTime", "Pax", "Assigned"), show="headings")
        for col in ("ID", "Origin", "Dest", "DepTime", "ArrTime", "Pax", "Assigned"):
            self.tree_fl.heading(col, text=col)
            self.tree_fl.column(col, anchor="center")
        sc_fl = ttk.Scrollbar(f_fl, orient="vertical", command=self.tree_fl.yview)
        self.tree_fl.configure(yscroll=sc_fl.set)
        self.tree_fl.pack(side="left", fill="both", expand=True)
        sc_fl.pack(side="right", fill="y")

        # --- Pestanya 3: Aeroports ---
        f_ap = tk.Frame(notebook, bg=self.C_PANEL)
        notebook.add(f_ap, text=" 📍 Base Aeroports ")
        self.tree_ap = ttk.Treeview(f_ap, columns=("Code", "Lat", "Lon"), show="headings")
        for c in ("Code", "Lat", "Lon"):
            self.tree_ap.heading(c, text=c)
            self.tree_ap.column(c, anchor="center")
        sc_ap = ttk.Scrollbar(f_ap, orient="vertical", command=self.tree_ap.yview)
        self.tree_ap.configure(yscroll=sc_ap.set)
        self.tree_ap.pack(side="left", fill="both", expand=True)
        sc_ap.pack(side="right", fill="y")

        # --- Pestanya 4: Mapa de Rutes i Eines ---
        f_tools = tk.Frame(notebook, bg=self.C_PANEL, padx=25, pady=25)
        notebook.add(f_tools, text=" 🗺️ Mapa i Final de Dia ")

        tk.Label(f_tools, text="Visualitzador Geolocalitzat de Rutes", font=("Segoe UI", 12, "bold"), fg=self.C_BLUE_ELECTRIC, bg=self.C_PANEL).pack(anchor="w", pady=(0, 5))
        tk.Label(f_tools, text="Selecciona una aeronau per generar el seu trajecte cartogràfic:", font=("Segoe UI", 9), fg=self.C_MUTED, bg=self.C_PANEL).pack(anchor="w", pady=(0, 10))

        route_sub = tk.Frame(f_tools, bg=self.C_PANEL)
        route_sub.pack(anchor="w", pady=(0, 20))
        tk.Label(route_sub, text="Avió:", bg=self.C_PANEL, fg=self.C_TEXT, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 10))
        self.combo_aircrafts = ttk.Combobox(route_sub, state="readonly", width=18)
        self.combo_aircrafts.pack(side="left", padx=5)

        btn_map = tk.Button(route_sub, text="🗺️ Dibuixar Ruta Geolocalitzada", bg=self.C_BLUE_ELECTRIC, fg="#0B132B", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=5, cursor="hand2", command=self.show_route_map)
        btn_map.pack(side="left", padx=10)

        tk.Frame(f_tools, height=1, bg=self.C_CARD).pack(fill="x", pady=15)

        tk.Label(f_tools, text="Estat de Flota a Final de Dia", font=("Segoe UI", 12, "bold"), fg=self.C_AMBER, bg=self.C_PANEL).pack(anchor="w", pady=(0, 5))
        tk.Label(f_tools, text="Calcula les posicions finals de cada avió i genera el fitxer per a l'endemà:", font=("Segoe UI", 9), fg=self.C_MUTED, bg=self.C_PANEL).pack(anchor="w", pady=(0, 10))

        btn_end = tk.Button(f_tools, text="💾 Generar 'aircrafts_end_of_day.txt'", bg=self.C_PURPLE, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8, cursor="hand2", command=self.save_end_day)
        btn_end.pack(anchor="w")

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=self.C_PANEL, height=25)
        footer.pack(fill="x", side="bottom")
        lbl = tk.Label(footer, text="AeroManager v2.0 | Developed for EETAC Systems Engineering", font=("Segoe UI", 8), fg=self.C_MUTED, bg=self.C_PANEL)
        lbl.pack(side="left", padx=15)

    def load_data(self):
        try:
            # Carrega usant el nom exacte del fitxer de la teva carpeta
            ac = LoadAircrafts("Aircrafts.txt")
            if not ac:
                ac = LoadAircrafts("aircrafts.txt")

            fl = LoadFlights("operations.txt")
            if not fl:
                fl = LoadFlights("flights.txt")

            ap = LoadAirports("airports.txt")
            if not ap:
                ap = LoadAirports("airports_saved.txt")

            if not ac and not fl:
                messagebox.showwarning("Atenció", "No s'han trobat fitxers de dades a la carpeta.")
                return

            self.airline = Airline("Vueling", ac, fl, ap)
            self.airports = ap

            # Actualitza valors del combo d'avions
            callsigns = [a.callsign for a in ac]
            self.combo_aircrafts['values'] = callsigns
            if callsigns:
                self.combo_aircrafts.current(0)

            self.update_tables()
            messagebox.showinfo("Èxit", f"Dades carregades correctament:\n• {len(ac)} Avions\n• {len(fl)} Vols\n• {len(ap)} Aeroports")
        except Exception as e:
            messagebox.showerror("Error", f"S'ha produït un error en carregar: {e}")

    def update_tables(self):
        if not self.airline:
            return

        # Netejar taules
        for r in self.tree_ac.get_children(): self.tree_ac.delete(r)
        for r in self.tree_fl.get_children(): self.tree_fl.delete(r)
        for r in self.tree_ap.get_children(): self.tree_ap.delete(r)

        # Taula d'Avions
        for a in self.airline.fleet:
            self.tree_ac.insert("", "end", values=(a.callsign, a.type, a.capacity, a.initial_airport))

        # Taula de Vols amb filtre
        filter_mode = self.combo_filter.get()
        assigned_count = 0
        for f in self.airline.operations:
            assigned = f.assigned_aircraft.callsign if f.assigned_aircraft else "NO ASSIGNAT"
            if f.assigned_aircraft:
                assigned_count += 1

            if filter_mode == "Només Assignats" and not f.assigned_aircraft:
                continue
            if filter_mode == "Només NO Assignats" and f.assigned_aircraft:
                continue

            self.tree_fl.insert("", "end", values=(f.id, f.departure_airport, f.arrival_airport, f.departure_time, f.arrival_time, f.passengers, assigned))

        # Taula d'Aeroports
        for ap in self.airports.values():
            self.tree_ap.insert("", "end", values=(ap.code, ap.latitude, ap.longitude))

        # Actualitzar KPI Cards
        self.card_fleet.value_label.config(text=str(len(self.airline.fleet)))
        self.card_flights.value_label.config(text=str(len(self.airline.operations)))
        self.card_assigned.value_label.config(text=f"{assigned_count} / {len(self.airline.operations)}")
        self.card_airports.value_label.config(text=str(len(self.airports)))

    def run_algo_a(self):
        if not self.airline:
            messagebox.showwarning("Atenció", "Prem primer el Pas 1 (Carregar Dades).")
            return
        AssignFlightsAlgorithmA(self.airline)
        self.update_tables()
        assigned = sum(1 for f in self.airline.operations if f.assigned_aircraft)
        messagebox.showinfo("Algorisme A Executat", f"Estratègia de 1 vol per avió completada.\nVols assignats: {assigned} de {len(self.airline.operations)}")

    def run_algo_b(self):
        if not self.airline:
            messagebox.showwarning("Atenció", "Prem primer el Pas 1 (Carregar Dades).")
            return
        AssignFlightsAlgorithmB(self.airline)
        self.update_tables()
        assigned = sum(1 for f in self.airline.operations if f.assigned_aircraft)
        messagebox.showinfo("Algorisme B Executat", f"Estratègia de fins a 2 vols per avió completada.\nVols assignats: {assigned} de {len(self.airline.operations)}")

    def show_comparison(self):
        if not self.airline:
            messagebox.showwarning("Atenció", "Carrega les dades abans de veure la comparativa.")
            return
        PlotFlightsComparison(self.airline)

    def show_route_map(self):
        if not self.airline:
            messagebox.showwarning("Atenció", "Carrega les dades primer.")
            return
        callsign = self.combo_aircrafts.get()
        if not callsign:
            messagebox.showwarning("Atenció", "Selecciona un avió.")
            return
        PlotAircraftRoutes(self.airline, callsign)

    def save_end_day(self):
        if not self.airline:
            messagebox.showwarning("Atenció", "Carrega les dades primer.")
            return
        end_locs = GetEndOfDayLocations(self.airline)
        updated_fleet = [Aircraft(a.callsign, a.type, a.capacity, end_locs[a.callsign]) for a in self.airline.fleet]
        SaveAircrafts(updated_fleet, "aircrafts_end_of_day.txt")
        messagebox.showinfo("Fitxer Generat", "S'ha creat 'aircrafts_end_of_day.txt' amb l'estat final de la flota per a l'endemà.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AeroManagerNavyDashboard(root)
    root.mainloop()