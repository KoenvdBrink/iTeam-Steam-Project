import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath("../AI"))

from steam_data_main import (
    get_player_summ,
    offline_for,
    last_logged_off,
    get_owned_games,
    is_online,
    most_played_games
)

def update_dashboard(steam_id, gui):
    try:
        profile_data = get_player_summ(steam_id)
        player = profile_data['response']['players'][0]
        name = player['personaname']
        online_status = "Online" if is_online(steam_id) else f"Offline sinds {offline_for(steam_id)} uur"
        last_logoff_time = last_logged_off(steam_id).strftime("%Y-%m-%d %H:%M:%S")

        # Top 5 meest gespeelde games (direct via most_played_games)
        top_games = most_played_games(steam_id, top_n=5)

        # Alle spellen (alleen namen voor nu)
        all_games = [game['name'] for game in get_owned_games(steam_id)[:15]]

        # Update GUI
        gui.update_labels(name, online_status, last_logoff_time)  # Alleen drie parameters
        gui.update_games_list(top_games)  # Top 5 games
        gui.update_all_games_list(all_games)  # Alle spellen

    except Exception:
        print(f"Fout bij ophalen van gegevens")
        

