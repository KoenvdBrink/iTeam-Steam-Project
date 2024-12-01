import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath("../AI"))

from steam_data_main import (
    get_player_summ,
    offline_for,
    last_logged_off,
    get_owned_games,
    is_online
)

def update_dashboard(steam_id, gui):
    try:
        profile_data = get_player_summ(steam_id)
        player = profile_data['response']['players'][0]
        name = player['personaname']
        online_status = "Online" if is_online(steam_id) else f"Offline sinds {offline_for(steam_id)} uur"
        last_logoff_time = last_logged_off(steam_id).strftime("%Y-%m-%d %H:%M:%S")

        top_games = []
        played_games = get_owned_games(steam_id) # Gebruik ter vervanging voor most_played_games
        for i, game in enumerate(played_games[:5], start=1): 
            top_games.append(f"{i}. {game['name']} - {game['playtime_forever'] // 60} uren gespeeld")

        # Alle spellen (alleen namen voor nu)
        all_games = [game['name'] for game in get_owned_games(steam_id)[:15]]

        # Update GUI
        gui.update_labels(name, online_status, last_logoff_time)  # Alleen drie parameters
        gui.update_games_list(top_games)  # Top 5 games
        gui.update_all_games_list(all_games)  # Alle spellen

    except Exception:
        print(f"Fout bij ophalen van gegevens")
        

