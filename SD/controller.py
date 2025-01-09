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

        # Update GUI zonder grafiek
        gui.update_labels(
            name,
            online_status,
            last_logoff_time,
            mdn_playtime,
            avg_playtime_2weeks
        )
        gui.update_games_list(top_games)

        # Start aparte thread voor het laden van de grafiek
        load_graph_in_thread(steam_id, gui)

    except Exception as e:
        print(f"Fout bij ophalen van gegevens: {e}")
        gui.set_error_message("Ongeldig Steam ID of fout bij ophalen van gegevens.")


def load_graph_in_thread(steam_id, gui):
    from threading import Thread

    def load_graph():
        try:
            # Toont 'Loading...' op de GUI
            def show_loading():
                gui.clear_graph_frame()
                gui.graph_label.config(text="Loading...")

            gui.root.after(0, show_loading)

            # Grafiekdata berekenen
            regression_data = collect_regression_data(steam_id)
            normalized_x, min_x, max_x = normalize_data([d["playtime_hours"] for d in regression_data])
            normalized_y, min_y, max_y = normalize_data([d["achievements_unlocked"] for d in regression_data])
            coefficients = gradient_descent(normalized_x, normalized_y)
            original_x = [d["playtime_hours"] for d in regression_data]
            original_y = [d["achievements_unlocked"] for d in regression_data]

            def update_gui():
                gui.graph_label.config(text="Playtime vs Achievements")
                gui.update_graph(normalized_x, normalized_y, original_x, original_y, coefficients)

            gui.root.after(0, update_gui)
        except Exception as e:
            print(f"Fout bij laden van grafiek: {e}")
            gui.root.after(0, lambda: gui.graph_label.config(text="Error loading graph"))

    # Start de thread
    Thread(target=load_graph).start()
