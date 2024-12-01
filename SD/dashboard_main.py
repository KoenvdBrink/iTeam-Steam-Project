import tkinter as tk
from gui import SteamDashboardGUI
from controller import update_dashboard

def update_dashboard_callback(steam_id):
    update_dashboard(steam_id, gui)

root = tk.Tk()
gui = SteamDashboardGUI(root, update_dashboard_callback)

root.mainloop()
