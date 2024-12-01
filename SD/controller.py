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
        print(f"Steam ID ontvangen: {steam_id}")
        profile_data = get_player_summ(steam_id)
        print(f"Profieldata ontvangen: {profile_data}")

        player = profile_data['response']['players'][0]
        name = player['personaname']
        online_status = "Online" if is_online(steam_id) else f"Offline sinds {offline_for(steam_id)} uur"

        # Gebruik fallback voor lastlogoff
        last_logoff_time = player.get('lastlogoff')
        if last_logoff_time:
            last_logoff_time = datetime.fromtimestamp(last_logoff_time).strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_logoff_time = "Niet beschikbaar"

        # Top 5 meest gespeelde games
        top_games = most_played_games(steam_id, top_n=5)

        # Alle spellen (alleen namen voor nu)
        all_games = [game['name'] for game in get_owned_games(steam_id)[:15]]

        # Update GUI
        gui.update_labels(name, online_status, last_logoff_time)
        gui.update_games_list(top_games)
        gui.update_all_games_list(all_games)

    except Exception as e:
        print(f"Fout bij ophalen van gegevens: {e}")
