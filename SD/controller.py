import sys
import os
from datetime import datetime
from threading import Thread
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
    gradient_descent,
    playtime_comparison
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
        mdn_playtime = round(median_playtime(steam_id) / 60, 1)
        avg_playtime_2weeks = round(average_playtime_2weeks(steam_id), 1)
        avg_playtime = round(average_playtime(steam_id) / 60, 1)

        # Top 20 meest gespeelde games
        top_games = most_played_games(steam_id, top_n=20)

        comparison_percentage = playtime_comparison(steam_id)
        if comparison_percentage < 100:
            comparison_text = (
                f"Gemiddeld, game jij {round(100 - comparison_percentage, 1)}% minder dan andere steam users."
            )
        else:
            comparison_text = (
                f"Gemiddeld, game jij {round(comparison_percentage - 100, 1)}% meer dan andere steam users."
            )

        # Update GUI zonder grafiek
        gui.update_labels(
            name,
            online_status,
            last_logoff_time,
            mdn_playtime,
            avg_playtime_2weeks,
            avg_playtime,
            comparison_text
        )
        gui.update_games_list(top_games)

        # Start aparte thread voor het laden van de grafiek
        load_graph_in_thread(steam_id, gui)

        # Start timer met dynamisch Steam ID
        start_timer_with_steam_id(steam_id)

    except Exception as e:
        print(f"Fout bij ophalen van gegevens: {e}")
        gui.set_error_message("Ongeldig Steam ID of fout bij ophalen van gegevens.")


def start_timer_status_thread(gui):
    """Start een thread om de timerstatus live bij te houden."""
    def run_status_updater():
        get_timer_status(gui.update_timer_status)

    thread = Thread(target=run_status_updater, daemon=True)
    thread.start()


def start_timer_with_steam_id(steam_id, gui):
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

        # Start checking status after starting timer
        start_timer_status_thread(gui)
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Fout bij uitvoeren van pc_serial.py: {e}")
    except FileNotFoundError as e:
        print(f"[ERROR] Bestand niet gevonden: {e}")
    except Exception as e:
        print(f"[ERROR] Onverwachte fout: {e}")


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
