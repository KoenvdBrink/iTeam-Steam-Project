import sys
import os
from datetime import datetime
import subprocess
sys.path.append(os.path.abspath("../AI"))

from steam_data_main import (
    get_player_summ,
    offline_for,
    last_logged_off,
    is_online,
    most_played_games,
    average_playtime,
    median_playtime,
    average_playtime_2weeks,
    collect_regression_data,
    normalize_data,
    gradient_descent
)


def update_dashboard(steam_id, gui):
    try:
        print(f"Steam ID ontvangen: {steam_id}")
        profile_data = get_player_summ(steam_id)
        print(f"Profieldata ontvangen: {profile_data}")

        player = profile_data['response']['players'][0]
        name = player['personaname']
        online_status = "Online" if is_online(steam_id) else f"Offline sinds {offline_for(steam_id)} uur"

        # Gebruik last_logged_off functie
        try:
            last_logoff_time = last_logged_off(steam_id).strftime("%Y-%m-%d %H:%M:%S")
        except (KeyError, AttributeError, TypeError) as e:
            print(f"Fout bij ophalen van lastlogoff: {e}")
            last_logoff_time = "Niet beschikbaar"

        # Gemiddelde speeltijd
        mdn_playtime = round(median_playtime(steam_id), 1)
        avg_playtime_2weeks = round(average_playtime_2weeks(steam_id), 1)

        # Top 20 meest gespeelde games
        top_games = most_played_games(steam_id, top_n=20)

        # Grafiekdata berekenen
        regression_data = collect_regression_data(steam_id)
        normalized_x, min_x, max_x = normalize_data([d["playtime_hours"] for d in regression_data])
        normalized_y, min_y, max_y = normalize_data([d["achievements_unlocked"] for d in regression_data])
        coefficients = gradient_descent(normalized_x, normalized_y)
        original_x = [d["playtime_hours"] for d in regression_data]
        original_y = [d["achievements_unlocked"] for d in regression_data]

        # Update GUI
        gui.update_labels(
            name,
            online_status,
            last_logoff_time,
            mdn_playtime,
            avg_playtime_2weeks
        )
        gui.update_games_list(top_games)
        gui.update_graph(normalized_x, normalized_y, original_x, original_y, coefficients)

        # Start timer met dynamisch Steam ID
        start_timer_with_steam_id(steam_id)

    except Exception as e:
        print(f"Fout bij ophalen van gegevens: {e}")


def start_timer_with_steam_id(steam_id):
    """Start pc_serial.py met een dynamisch Steam ID."""
    try:
        # Dynamisch pad bepalen naar pc_serial.py
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TI/pc_serial.py"))

        # Controleer of het bestand bestaat
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Bestand niet gevonden op pad: {script_path}")

        # Voer het script uit en geef het Steam ID mee
        subprocess.run(["python", script_path, steam_id], check=True)
        print(f"[INFO] Timer gestart met Steam ID: {steam_id}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Fout bij uitvoeren van pc_serial.py: {e}")
    except FileNotFoundError as e:
        print(f"[ERROR] Bestand niet gevonden: {e}")
    except Exception as e:
        print(f"[ERROR] Onverwachte fout: {e}")
