import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SteamDashboardGUI:
    def __init__(self, root, update_callback):
        self.root = root
        self.update_callback = update_callback

        # Kleuren
        self.bg_color = "#1b2838"
        self.text_color = "#c7d5e0"
        self.accent_color = "#66c0f4"

        self.root.title("Steam Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.bg_color)

        # Main frame en grid layout
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Rijen en columns aangemaakt
        for col in range(3):
            self.main_frame.grid_columnconfigure(col, weight=1)
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

        # Steam ID invoerveld gecentreerd
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

        self.name_label = tk.Label(
            self.main_frame, text="Naam: -", font=("Arial", 14),
            bg=self.bg_color, fg=self.text_color
        )
        self.name_label.grid(row=5, column=0, sticky="w", padx=10)

        self.status_label = tk.Label(
            self.main_frame, text="Status: -", font=("Arial", 14),
            bg=self.bg_color, fg=self.text_color
        )
        self.status_label.grid(row=6, column=0, sticky="w", padx=10)

        self.last_logoff_label = tk.Label(
            self.main_frame, text="Laatst uitgelogd: -", font=("Arial", 14),
            bg=self.bg_color, fg=self.text_color
        )
        self.last_logoff_label.grid(row=7, column=0, sticky="w", padx=10)

        # Kolom 1: Top 5 games
        self.games_label = tk.Label(
            self.main_frame, text="Top 5 meest gespeelde games:", font=("Arial", 16, "bold"),
            bg=self.bg_color, fg=self.accent_color
        )
        self.games_label.grid(row=4, column=1, sticky="n", padx=10, pady=(20, 5))

        self.games_list = tk.Listbox(
            self.main_frame, width=40, height=10, font=("Arial", 12),
            bg="#2a475e", fg=self.text_color, highlightbackground=self.bg_color, bd=0
        )
        self.games_list.grid(row=5, column=1, rowspan=12, sticky="nsew", padx=10, pady=5)

        # Kolom 2: All games
        self.all_games_label = tk.Label(
            self.main_frame, text="Alle spellen:", font=("Arial", 16, "bold"),
            bg=self.bg_color, fg=self.accent_color
        )
        self.all_games_label.grid(row=4, column=2, sticky="n", padx=10, pady=(20, 5))

        self.all_games_list = tk.Listbox(
            self.main_frame, width=40, height=20, font=("Arial", 12),
            bg="#2a475e", fg=self.text_color, highlightbackground=self.bg_color, bd=0
        )
        self.all_games_list.grid(row=5, column=2, rowspan=12, sticky="nsew", padx=10, pady=5)

    def on_submit(self):
        steam_id = self.steam_id_entry.get()
        if steam_id:
            self.update_callback(steam_id)

    def update_labels(self, name, status, last_logoff):
        self.name_label.config(text=f"Naam: {name}")
        self.status_label.config(text=f"Status: {status}")
        self.last_logoff_label.config(text=f"Laatst uitgelogd: {last_logoff}")

    def update_games_list(self, games):
        self.games_list.delete(0, tk.END)
        for game in games:
            self.games_list.insert(tk.END, game)

    def update_all_games_list(self, games):
        self.all_games_list.delete(0, tk.END)
        for game in games:
            self.all_games_list.insert(tk.END, game)
