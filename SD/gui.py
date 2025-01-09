import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SteamDashboardGUI:
    def __init__(self, root, update_callback):
        self.root = root
        self.update_callback = update_callback

        # Kleuren
        self.bg_color = "#1b2838"
        self.text_color = "#c7d5e0"
        self.accent_color = "#66c0f4"
        self.error_color = "#FF0000"

        self.root.title("Steam Dashboard")
        self.root.geometry("1400x800")
        self.root.configure(bg=self.bg_color)

        # Main frame en grid layout
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Vaste kolombreedtes
        self.main_frame.grid_columnconfigure(0, weight=0, minsize=300)  # Kolom 0: vaste breedte
        self.main_frame.grid_columnconfigure(1, weight=1, minsize=500)  # Kolom 1: flexibele breedte
        self.main_frame.grid_columnconfigure(2, weight=1, minsize=600)  # Kolom 2: grafiek

        for row in range(20):
            self.main_frame.grid_rowconfigure(row, weight=0, minsize=20)

        # Logo
        try:
            logo_image = Image.open("steam_logo.png")
            logo_image = logo_image.resize((120, 120), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_image)
            self.logo_label = tk.Label(self.main_frame, image=self.logo, bg=self.bg_color)
            self.logo_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        except Exception as e:
            self.logo_label = tk.Label(
                self.main_frame, text="Logo niet gevonden", bg=self.bg_color, fg="red", font=("Arial", 12)
            )
            self.logo_label.grid(row=0, column=0, sticky="w", padx=20, pady=50)
            print(f"Fout bij laden van logo: {e}")

        # Titel "Steam Dashboard"
        self.title_label = tk.Label(
            self.main_frame, text="Steam Dashboard", font=("Arial", 28, "bold"),
            bg=self.bg_color, fg=self.accent_color
        )
        self.title_label.grid(row=0, column=1, sticky="n", pady=50)

        # Steam ID invoerveld
        self.error_label = tk.Label(
            self.main_frame, text="", font=("Arial", 12), bg=self.bg_color, fg=self.error_color
        )
        self.error_label.grid(row=0, column=1, sticky="n", pady=(5, 5))

        self.steam_id_label = tk.Label(
            self.main_frame, text="Voer Steam ID in:", font=("Arial", 14),
            bg=self.bg_color, fg=self.text_color
        )
        self.steam_id_label.grid(row=1, column=1, sticky="n", pady=(10, 5))

        self.steam_id_entry = tk.Entry(
            self.main_frame, font=("Arial", 12), width=30
        )
        self.steam_id_entry.grid(row=2, column=1, sticky="n", pady=(5, 5))

        self.steam_id_button = tk.Button(
            self.main_frame, text="Ophalen", font=("Arial", 12),
            command=self.on_submit
        )
        self.steam_id_button.grid(row=3, column=1, sticky="n", pady=(5, 20))

        # Kolom 0: Accountinformatie
        self.account_info_label = tk.Label(
            self.main_frame, text="Accountinformatie", font=("Arial", 16, "bold"),
            bg=self.bg_color, fg=self.accent_color
        )
        self.account_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=(20, 5))

        small_font = ("Arial", 12)
        self.name_label = tk.Label(
            self.main_frame, text="Naam: -", font=small_font,
            bg=self.bg_color, fg=self.text_color
        )
        self.name_label.grid(row=5, column=0, sticky="w", padx=10)

        self.status_label = tk.Label(
            self.main_frame, text="Status: -", font=small_font,
            bg=self.bg_color, fg=self.text_color
        )
        self.status_label.grid(row=6, column=0, sticky="w", padx=10)

        self.last_logoff_label = tk.Label(
            self.main_frame, text="Laatst uitgelogd: -", font=small_font,
            bg=self.bg_color, fg=self.text_color
        )
        self.last_logoff_label.grid(row=7, column=0, sticky="w", padx=10)

        self.median_playtime_label = tk.Label(
            self.main_frame, text="Mediaan speeltijd: -", font=small_font,
            bg=self.bg_color, fg=self.text_color
        )
        self.median_playtime_label.grid(row=8, column=0, sticky="w", padx=10)

        self.average_playtime_2weeks_label = tk.Label(
            self.main_frame, text="Gem. speeltijd (2 weken): -", font=small_font,
            bg=self.bg_color, fg=self.text_color
        )
        self.average_playtime_2weeks_label.grid(row=9, column=0, sticky="w", padx=10)

        # Kolom 1: Top 20 games
        self.games_label = tk.Label(
            self.main_frame, text="Top 20 meest gespeelde games:", font=("Arial", 16, "bold"),
            bg=self.bg_color, fg=self.accent_color
        )
        self.games_label.grid(row=4, column=1, sticky="n", padx=10, pady=(20, 5))

        self.games_list = tk.Listbox(
            self.main_frame, width=40, height=10, font=("Arial", 12),
            bg="#2a475e", fg=self.text_color, highlightbackground=self.bg_color, bd=0
        )
        self.games_list.grid(row=5, column=1, rowspan=12, sticky="nsew", padx=10, pady=5)

        # Kolom 2: Grafiek
        self.graph_label = tk.Label(
            self.main_frame, text="Playtime vs Achievements", font=("Arial", 16, "bold"),
            bg=self.bg_color, fg=self.accent_color
        )
        self.graph_label.grid(row=4, column=2, sticky="n", padx=10, pady=(20, 5))

        self.graph_frame = tk.Frame(
            self.main_frame, bg=self.bg_color, bd=2, relief="ridge", width=600, height=400
        )
        self.graph_frame.grid(row=5, column=2, rowspan=12, sticky="nsew", padx=10, pady=5)
        self.graph_frame.grid_propagate(False)
        self.placeholder_label = tk.Label(
            self.graph_frame, text="Voer uw steam ID in", bg=self.bg_color, fg=self.text_color, font=("Arial", 12)
        )
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_submit(self):
        steam_id = self.steam_id_entry.get()
        if steam_id:
            self.set_error_message("")
            self.update_callback(steam_id)

    def set_error_message(self, message):
        self.error_label.config(text=message)

    def update_labels(self, name, status, last_logoff, mdn_playtime, avg_playtime_2weeks): # avg_playtime tijdelijk weg gehaalt voor testen.
        self.name_label.config(text=f"Naam: {name}")
        self.status_label.config(text=f"Status: {status}")
        self.last_logoff_label.config(text=f"Laatst uitgelogd: {last_logoff}")
        self.median_playtime_label.config(text=f"Mediaan speeltijd: {mdn_playtime} uur")
        self.average_playtime_2weeks_label.config(text=f"Gem. speeltijd (2 weken): {avg_playtime_2weeks} minuten")
        # self.average_playtime_label.config(text=f"Totale speeltijd: {avg_playtime} uur")

    def update_games_list(self, games):
        self.games_list.delete(0, tk.END)
        for game in games:
            self.games_list.insert(tk.END, game)

    def update_graph(self, normalized_x, normalized_y, original_x, original_y, coefficients):
        self.clear_graph_frame()
    
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.bg_color)
        regression_line = [coefficients[0] + coefficients[1] * xi for xi in normalized_x]

        ax.scatter(normalized_x, normalized_y, color="#66c0f4", alpha=0.7, s=15, label="Data Points")
        ax.plot(normalized_x, regression_line, color="#FF0000", label="Regression Line")

        ax.set_facecolor("#171a21")
        ax.spines['bottom'].set_color("#8f98a0")
        ax.spines['left'].set_color("#8f98a0")
        ax.tick_params(colors="#c7d5e0")
        ax.legend(facecolor="#171a21", edgecolor="#8f98a0", labelcolor="#c7d5e0")
        ax.set_title("Playtime vs Achievements", color="#c7d5e0")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_graph_frame(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
