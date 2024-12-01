import tkinter as tk
from gui import SteamDashboardGUI
from controller import update_dashboard

STEAM_ID = "76561198055954925"  # Testing steamIDs van Koen

def update_dashboard_callback():
    update_dashboard(STEAM_ID, gui)

root = tk.Tk()
gui = SteamDashboardGUI(root, update_dashboard_callback)

# Directe update bij opstarten
update_dashboard_callback()

root.mainloop()
