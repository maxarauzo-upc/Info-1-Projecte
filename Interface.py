# interface.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from aircraft import LoadAircrafts
from flight import LoadFlights
from airline import Airline, PlotFlights


class AirlineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AeroManager - Gestió d'Operacions d'Aerolínia")
        self.root.geometry("850x620")
        self.root.minsize(800, 550)

        # Configuració del tema i colors corporatius
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.BG_MAIN = "#F4F6F9"
        self.NAV_BAR = "#1E293B"
        self.ACCENT_COLOR = "#0284C7"
        self.TEXT_COLOR = "#0F172A"

        self.root.configure(bg=self.BG_MAIN)
        self.airline = None

        self._configure_styles()
        self._build_header()
        self._build_dashboard_summary()
        self._build_main_content()
        self._build_footer()

    def _configure_styles(self):
        # Configuració d'estils visuals per a ttk
        self.style.configure("TNotebook", background=self.BG_MAIN, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#E2E8F0", foreground=self.TEXT_COLOR,
                             padding=[15, 6], font=("Helvetica", 10, "bold"), borderwidth=0)
        self.style.map("TNotebook.Tab", background=[("selected", self.ACCENT_COLOR)],
                       foreground=[("selected", "#FFFFFF")])

        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"),
                             background="#E2E8F0", foreground=self.TEXT_COLOR)
        self.style.configure("Treeview", font=("Helvetica", 9), rowheight=25)

    def _build_header(self):
        # Barra superior (Header)
        header = tk.Frame(self.root, bg=self.NAV_BAR, height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Carregar el logo de la universitat si existeix
        logo_loaded = False
        for ext in [".png", ".jpg", ".jpeg"]:
            logo_path = f"logo{ext}"
            if os.path.exists(logo_path):
                try:
                    img = Image.open(logo_path)
                    img = img.resize((140, 50), Image.Resampling.LANCZOS)
                    self.logo_img = ImageTk.PhotoImage(img)
                    logo_label = tk.Label(header, image=self.logo_img, bg=self.NAV_BAR)
                    logo_label.pack(side="left", padx=20, pady=10)
                    logo_loaded = True
                    break
                except Exception:
                    pass

        if not logo_loaded:
            lbl_logo_fallback = tk.Label(header, text="UNIVERSITAT", font=("Helvetica", 12, "bold"),
                                         fg="#94A3B8", bg=self.NAV_BAR)
            lbl_logo_fallback.pack(side="left", padx=20)

        # Títol del sistema
        lbl_title = tk.Label(header, text="AeroManager System", font=("Helvetica", 18, "bold"),
                             fg="#FFFFFF", bg=self.NAV_BAR)
        lbl_title.pack(side="left", padx=10)

    def _build_dashboard_summary(self):
        # Targeta d'estat i accions principals
        action_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid")
        action_frame.pack(fill="x", padx=20, pady=15)

        # Panell esquerra: Informació
        info_subframe = tk.Frame(action_frame, bg="#FFFFFF")
        info_subframe.pack(side="left", padx=15, pady=12)

        lbl_status_title = tk.Label(info_subframe, text="Estat de l'Aerolínia", font=("Helvetica", 9, "bold"),
                                    fg="#64748B", bg="#FFFFFF")
        lbl_status_title.pack(anchor="w")

        self.lbl_info = tk.Label(info_subframe, text="Cap dada carregada", font=("Helvetica", 12, "bold"),
                                 fg=self.TEXT_COLOR, bg="#FFFFFF")
        self.lbl_info.pack(anchor="w")

        # Panell dreta: Botons d'acció
        btn_subframe = tk.Frame(action_frame, bg="#FFFFFF")
        btn_subframe.pack(side="right", padx=15, pady=10)

        btn_load = tk.Button(btn_subframe, text="Carregar Dades", font=("Helvetica", 10, "bold"),
                             bg=self.ACCENT_COLOR, fg="white", activebackground="#0369A1",
                             activeforeground="white", relief="flat", padx=15, pady=6, cursor="hand2",
                             command=self.load_data)
        btn_load.pack(side="left", padx=5)

        btn_plot = tk.Button(btn_subframe, text="📊 Analitzar Vols", font=("Helvetica", 10, "bold"),
                             bg="#10B981", fg="white", activebackground="#059669",
                             activeforeground="white", relief="flat", padx=15, pady=6, cursor="hand2",
                             command=self.show_plot)
        btn_plot.pack(side="left", padx=5)

    def _build_main_content(self):
        # Secció central amb pestanyes
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # --- Pestanya 1: Flota d'Avions ---
        frame_aircrafts = tk.Frame(notebook, bg="#FFFFFF")
        notebook.add(frame_aircrafts, text=" Flota d'Avions ")

        self.tree_aircrafts = ttk.Treeview(frame_aircrafts, columns=("Callsign", "Type", "Capacity"), show="headings")
        self.tree_aircrafts.heading("Callsign", text="Callsign")
        self.tree_aircrafts.heading("Type", text="Model d'Avió")
        self.tree_aircrafts.heading("Capacity", text="Capacitat (Passatgers)")

        self.tree_aircrafts.column("Callsign", anchor="center", width=150)
        self.tree_aircrafts.column("Type", anchor="center", width=200)
        self.tree_aircrafts.column("Capacity", anchor="center", width=150)

        scroll_ac = ttk.Scrollbar(frame_aircrafts, orient="vertical", command=self.tree_aircrafts.yview)
        self.tree_aircrafts.configure(yscroll=scroll_ac.set)

        self.tree_aircrafts.pack(side="left", fill="both", expand=True)
        scroll_ac.pack(side="right", fill="y")

        # --- Pestanya 2: Operacions / Vols ---
        frame_flights = tk.Frame(notebook, bg="#FFFFFF")
        notebook.add(frame_flights, text=" Operacions de Vol ")

        self.tree_flights = ttk.Treeview(frame_flights,
                                         columns=("ID", "Origin", "Dest", "DepTime", "ArrTime", "Passengers"),
                                         show="headings")
        self.tree_flights.heading("ID", text="Codi Vol")
        self.tree_flights.heading("Origin", text="Origen (ICAO)")
        self.tree_flights.heading("Dest", text="Destí (ICAO)")
        self.tree_flights.heading("DepTime", text="Sortida")
        self.tree_flights.heading("ArrTime", text="Arribada")
        self.tree_flights.heading("Passengers", text="Passatgers")

        for col in ("ID", "Origin", "Dest", "DepTime", "ArrTime", "Passengers"):
            self.tree_flights.column(col, anchor="center", width=100)

        scroll_fl = ttk.Scrollbar(frame_flights, orient="vertical", command=self.tree_flights.yview)
        self.tree_flights.configure(yscroll=scroll_fl.set)

        self.tree_flights.pack(side="left", fill="both", expand=True)
        scroll_fl.pack(side="right", fill="y")

    def _build_footer(self):
        # Peu de pàgina formal
        footer = tk.Frame(self.root, bg="#E2E8F0", height=25)
        footer.pack(fill="x", side="bottom")

        lbl_footer = tk.Label(footer, text="Sistema de Gestió d'Aerolínies v1.0 | Grau en Enginyeria",
                              font=("Helvetica", 8), fg="#64748B", bg="#E2E8F0")
        lbl_footer.pack(side="left", padx=10)

    def load_data(self):
        try:
            aircrafts = LoadAircrafts("aircrafts.txt")
            flights = LoadFlights("operations.txt")

            if not aircrafts and not flights:
                messagebox.showwarning("Atenció", "No s'han trobat dades als fitxers 'aircrafts.txt' o 'operations.txt'.")
                return

            self.airline = Airline("Vueling", aircrafts, flights)
            self.lbl_info.config(
                text=f"Aerolínia: {self.airline.name}  |  Avions: {len(self.airline.fleet)}  |  Vols: {len(self.airline.operations)}")

            # Netejar taules
            for row in self.tree_aircrafts.get_children():
                self.tree_aircrafts.delete(row)
            for row in self.tree_flights.get_children():
                self.tree_flights.delete(row)

            # Omplir taula d'avions
            for a in self.airline.fleet:
                self.tree_aircrafts.insert("", "end", values=(a.callsign, a.type, a.capacity))

            # Omplir taula de vols
            for f in self.airline.operations:
                self.tree_flights.insert("", "end",
                                         values=(f.id, f.departure_airport, f.arrival_airport, f.departure_time,
                                                 f.arrival_time, f.passengers))

            messagebox.showinfo("Èxit", "S'han carregat totes les dades correctament!")
        except Exception as e:
            messagebox.showerror("Error", f"Error en carregar les dades: {e}")

    def show_plot(self):
        if self.airline is None:
            messagebox.showwarning("Atenció", "Carrega primer les dades de l'aerolínia per generar el gràfic.")
            return
        PlotFlights(self.airline)


if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineApp(root)
    root.mainloop()