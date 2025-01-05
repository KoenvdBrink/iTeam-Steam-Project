import requests
import pandas as pd
from tqdm import tqdm

# Function to fetch all games data from SteamSpy
def fetch_steam_games():
    url = "https://steamspy.com/api.php?request=all"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error fetching SteamSpy data: {e}")
        return {}

# Fetch data
print("Fetching game data from SteamSpy...")
all_games = fetch_steam_games()

# Prepare a list to store filtered games
filtered_games = []

# Process each game and filter by peak players (>= 1000)
if all_games:
    print("Filtering games with peak players >= 500...")
    for app_id, game_data in tqdm(all_games.items(), desc="Processing games"):
        if game_data.get("ccu", 0) >= 50:  # "ccu" = current concurrent users (proxy for peak players)
            filtered_games.append({
                "app_id": app_id,
                "name": game_data.get("name"),
                "peak_players": game_data.get("ccu")
            })

# Convert to DataFrame
filtered_df = pd.DataFrame(filtered_games)

# Save to CSV or print the results
if not filtered_df.empty:
    filtered_df.to_csv("filtered_steam_games.csv", index=False)
    print("Filtered games saved to 'filtered_steam_games.csv'")
else:
    print("No games found with peak players >= 1000.")
