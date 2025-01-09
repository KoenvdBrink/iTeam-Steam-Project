from operator import itemgetter
import requests
import datetime
from datetime import datetime
import csv
import steamspypi
from tqdm import tqdm
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from Fetch_data_server import fetch_average_playtime


input_file = "filtered_steam_games.csv"
output_file = "app_details.csv"
api_key = "5409DBECBF319D8375208A2EC86A66FE"
koen = "76561198030044972"
zack = "76561198055954925"
nizar = "76561198266159443"
gamer = "76561198056739081"
app_ids = []
user_scores = []
peak_players = []


def get_player_summ(steam_id):
    """
    Returns basic profile information for a given 64-bit Steam ID.

    :param steam_id: str, Steam user's 64-bit ID
    :return: dict containing profile information
    """
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    params = {
        'key':api_key,
        'steamids':steam_id
    }
    response = requests.get(url, params=params)
    return response.json()

def get_owned_games(steam_id):
    """
    Returns a list of owned games sorted by playtime in descending order.

    :param steam_id: str, Steam user's 64-bit ID
    :return: list of dicts, each containing game details
    """
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': api_key,
        'steamid': steam_id,
        'include_appinfo': True,
        'format': 'json'
    }
    response = requests.get(url, params=params).json()
    if 'response' in response and 'games' in response['response']:
        played_games = sorted(response['response']['games'], key=itemgetter('playtime_forever'), reverse=True)
        return played_games

    return []

def last_logged_off(steam_id):
    """
    Returns the datetime of the user's last logoff.

    :param steam_id: str, Steam user's 64-bit ID
    :return: datetime of last logoff
    """
    time_unix = get_player_summ(steam_id)['response']['players'][0]['lastlogoff']
    return datetime.fromtimestamp(time_unix)

def offline_for(steam_id):
    """
    Calculates the number of hours since the user last logged off.

    :param steam_id: str, Steam user's 64-bit ID
    :return: int, hours since last logoff, or -1 if online
    """
    user_data = get_player_summ(steam_id)['response']['players'][0]
    if user_data['personastate'] != 0:
        return -1
    last_logoff_time = datetime.fromtimestamp(user_data['lastlogoff'])
    hours_offline = int((datetime.now() - last_logoff_time).total_seconds() // 3600)
    return hours_offline

def most_played_games(steam_id, top_n=5):
    """
    Prints the user's top N most played games.

    :param steam_id: str, Steam user's 64-bit ID
    :param top_n: int, number of top games to display
    """
    played_games = get_owned_games(steam_id)
    top_games = played_games[:top_n]
    result = []
    for i, game in enumerate(top_games, start=1):
        result.append(f"{i}. {game['name']} - {game['playtime_forever'] // 60} uren gespeeld")
        
    return result

def is_online(steam_id):
    """
    Checks if user is online.
    :param steam_id: str, Steam user's 64-bit ID
    :return: Boolean, True if user is online, False if user is offline
    """
    user_data = get_player_summ(steam_id)['response']['players'][0]
    if user_data['personastate'] != 0:
        return True
    else:
        return False

def get_app_info(app_id):
    """

    :param app_id:
    :return:
    """
    url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url).json()
    app_data = response.get(str(app_id))
    data = app_data.get('data', {})
    return data

def average_playtime(steam_id):
    """
    Calculates the average minutes the user has played the games in their library with more than 60 minutes played.
    :param steam_id: str, Steam user's 64-bit ID
    :return: int, Average playtime in minutes
    """
    user_data = get_owned_games(steam_id)
    played_games = 0
    total_played = 0
    for game in user_data:
        if game['playtime_forever'] < 1:
            break
        else:
            played_games += 1
            total_played += int(game['playtime_forever'])
    if played_games == 0:
        return 0
    return int(total_played / played_games)

def median_playtime(steam_id):
    """
    Calculates the median gametime (in minutes) the user has played all the games
    with more thatn 60 minutes gametime in their steam library
    :param steam_id:
    :return: int, median gametime in minutes
    """
    user_data = get_owned_games(steam_id)
    gametime = []
    games = []
    median = None
    for game in user_data:
        if game['playtime_forever'] < 1:
            break
        else:
            games.append(game['name'])
            gametime.append(int(game['playtime_forever']))
    gametime.sort()
    n = len(gametime)
    if n % 2 == 0:
        median = (gametime[n//2 - 1] + gametime[n//2]) / 2
    else:
        median = gametime[n // 2]
    return median

def get_metacritic_score(app_id):
    """

    :param app_id:
    :return:
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data[str(app_id)]['success']:
            app_data = data[str(app_id)]['data']
            metacritic = app_data.get('metacritic')
            if metacritic:
                return metacritic['score']
            else:
                return None
    return None

def get_player_count(appid):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("response", {}).get("player_count", 0)  # Returns player count or 0 if not found
    else:
        print(f"Failed to fetch player count for appid {appid}.")
        return 0

def get_playtime_for_app(steam_id, app_id):
    """
    Returns the average playtime (in hours) for a specific appID if the user owns it.

    :param steam_id: str, Steam user's 64-bit ID
    :param app_id: int, The appID of the game
    :return: float, Average playtime in hours, or 0 if the game is not owned
    """
    owned_games = get_owned_games(steam_id)
    for game in owned_games:
        if game['appid'] == app_id:
            playtime_minutes = game['playtime_forever']
            playtime_hours = playtime_minutes / 60  # Convert to hours
            return round(playtime_hours, 2)
    return 0  # Game not owned or no playtime recorded

def read_app_ids_from_csv(input_file):
    """
    Reads app IDs from a CSV file and returns them as a list of integers.

    :param input_file: str, Path to the CSV file.
    :return: list of int, List of app IDs.
    """
    app_ids = []
    with open(input_file, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            app_ids.append(int(row['app_id']))  # Convert to int
    return app_ids

def fetch_app_details(app_ids, output_file="app_details.csv"):
    """
    Fetches average playtime, median playtime, user score, and peak concurrent players
    for a list of app IDs and writes the data to a CSV file, with a progress bar.

    :param app_ids: list of int, Steam app IDs.
    :param output_file: str, Path to the output CSV file.
    """
    app_data_list = []

    # Progress bar for app IDs
    for app_id in tqdm(app_ids, desc="Fetching App Details"):
        # Create the request
        data_request = {
            'request': 'appdetails',
            'appid': str(app_id)
        }

        try:
            # Fetch the data
            data = steamspypi.download(data_request)

            # Check if data exists
            if not data:
                print(f"No data found for app ID {app_id}")
                continue

            # Extract required fields
            app_name = data.get('name', 'Unknown')
            avg_playtime = data.get('average_forever', 0)  # Average playtime (minutes)
            median_playtime = data.get('median_forever', 0)  # Median playtime (minutes)
            positive = data.get('positive', 0)
            negative = data.get('negative', 0)

            # Fetch peak players using your get_player_count function
            peak_players = get_player_count(app_id)

            # Calculate userscore manually
            total_reviews = positive + negative
            user_score = (positive / total_reviews) * 100 if total_reviews > 0 else 0

            # Append data to the list
            app_data_list.append({
                'AppID': app_id,
                'Name': app_name,
                'Average Playtime (hrs)': round(avg_playtime / 60, 2),  # Convert to hours
                'Median Playtime (hrs)': round(median_playtime / 60, 2),  # Convert to hours
                'User Score (%)': round(user_score, 2),  # Manually calculated userscore
                'Peak Players': peak_players  # Peak concurrent players
            })

        except Exception as e:
            print(f"Error fetching data for app ID {app_id}: {e}")
            continue

    # Write data to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['AppID', 'Name', 'Average Playtime (hrs)', 'Median Playtime (hrs)', 'User Score (%)',
                      'Peak Players']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(app_data_list)

    print(f"Data written to {output_file}")

def normalize_data(data):
    """
    Normalizes a list of values and returns the normalized data,
    along with the min and max values used for normalization.

    :param data: list of numbers.
    :return: tuple (normalized_data, min_val, max_val).
    """
    min_val = min(data)
    max_val = max(data)
    normalized_data = [(x - min_val) / (max_val - min_val) for x in data]
    return normalized_data, min_val, max_val

def gradient_descent(x, y, num_iterations=1000, learning_rate=0.001):
    c = [0, 0]
    for i in range(num_iterations):
        for i in range(len(x)):
            prediction = c[0] + c[1] * x[i]
            error = prediction - y[i]
            c[0] -= error * learning_rate
            c[1] -= error * x[i] * learning_rate
    return c

def average_playtime_2weeks(steam_id):
    """
    Calculates the average minutes per day the user has played games in their steam library over the last 14 days.
    :param steam_id: str, Steam user's 64-bit ID
    :return: int, Average playtime in minutes
    """
    user_data = get_owned_games(steam_id)
    time_played = 0
    for data in user_data:
        if 'playtime_2weeks' in data:
            time_played += data['playtime_2weeks']
    return (time_played / 14)

def fetch_game_data(game, steam_id):
    """
    Fetches playtime and achievements for a single game,
    excluding games with 0 achievements.

    :param game: dict, Game data from owned games API.
    :param steam_id: str, Steam user's 64-bit ID.
    :return: dict, Processed game data with achievements.
    """
    playtime_hours = game['playtime_forever'] / 60
    if playtime_hours < 1:  # Skip games with less than 1 hour of playtime
        return None

    achievements = get_game_achievements(steam_id, game['appid'])
    if achievements == 0:  # Skip games with 0 achievements
        return None

    return {
        "game_id": game['appid'],
        "game_name": game['name'],
        "playtime_hours": playtime_hours,
        "achievements_unlocked": achievements,
    }

def get_game_achievements(steam_id, app_id):
    url = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "appid": app_id,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        achievements = response.json().get("playerstats", {}).get("achievements", [])
        return len(achievements)  # Count of unlocked achievements
    return 0

def filter_outliers_iqr(data, key="playtime_hours"):
    """
    Filters outliers in a dataset based on the IQR method.

    :param data: list of dicts, the dataset.
    :param key: str, the key to filter by (e.g., "playtime_hours").
    :return: list of dicts, filtered dataset.
    """
    values = [d[key] for d in data]
    q1 = np.percentile(values, 25)  # 25th percentile
    q3 = np.percentile(values, 75)  # 75th percentile
    iqr = q3 - q1  # Interquartile Range

    # Define the outlier bounds
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Filter out outliers
    filtered_data = [d for d in data if lower_bound <= d[key] <= upper_bound]
    return filtered_data

def collect_regression_data(steam_id, max_games=1000):
    """
    Collects total playtime and achievements for the top N most played games in parallel,
    excluding games with 0 achievements and filtering out outliers using the IQR method.

    :param steam_id: str, Steam user's 64-bit ID.
    :param max_games: int, Maximum number of games to process.
    :return: list of dicts containing playtime and achievements data.
    """
    owned_games = get_owned_games(steam_id)[:max_games]

    regression_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_game_data, game, steam_id) for game in owned_games]
        for future in tqdm(futures, desc="Fetching Game Data"):
            result = future.result()
            if result:
                regression_data.append(result)

    # Filter out outliers based on playtime using the IQR method
    filtered_data = filter_outliers_iqr(regression_data, key="playtime_hours")

    return filtered_data

def prepare_regression_data(data):
    """
    Normalizes playtime and achievements for regression.

    :param data: list of dicts with playtime and achievements
    :return: normalized X and Y arrays
    """
    playtime = [d["playtime_hours"] for d in data]
    achievements = [d["achievements_unlocked"] for d in data]

    normalized_playtime = normalize_data(playtime)
    normalized_achievements = normalize_data(achievements)

    return normalized_playtime, normalized_achievements

def plot_regression(normalized_x, normalized_y, original_x, original_y, coefficients):
    """
    Plots the regression data using normalized data but displays non-normalized axis labels.
    Uses a Steam-inspired color scheme.

    :param normalized_x: Independent variable (normalized playtime)
    :param normalized_y: Dependent variable (normalized achievements)
    :param original_x: Independent variable (original playtime in hours)
    :param original_y: Dependent variable (original achievements unlocked)
    :param coefficients: Regression coefficients (computed using normalized data)
    """
    # Generate the regression line using normalized data
    regression_line = [coefficients[0] + coefficients[1] * xi for xi in normalized_x]

    # Set the Steam-inspired colors
    background_color = "#171a21"  # Dark blue/gray
    text_color = "#c7d5e0"        # Light gray
    scatter_color = "#66c0f4"     # Cyan
    line_color = "#FF0000"        # Bright teal
    grid_color = "#8f98a0"        # Muted gray

    # Set the figure background
    plt.figure(figsize=(8, 6), facecolor=background_color)
    ax = plt.gca()
    ax.set_facecolor(background_color)

    # Plot the scatter points and regression line
    plt.scatter(normalized_x, normalized_y, color=scatter_color, alpha=0.7, s=15, label="Data Points")
    plt.plot(normalized_x, regression_line, color=line_color, label="Regression Line")

    # Get tick positions for normalized data within the range [0, 1]
    valid_xticks = [t for t in plt.xticks()[0] if 0 <= t <= 1]
    valid_yticks = [t for t in plt.yticks()[0] if 0 <= t <= 1]

    # Map valid normalized ticks back to original data range
    original_x_ticks = [min(original_x) + (max(original_x) - min(original_x)) * t for t in valid_xticks]
    original_y_ticks = [min(original_y) + (max(original_y) - min(original_y)) * t for t in valid_yticks]

    # Set custom tick labels with formatted original values
    plt.xticks(valid_xticks, [f"{tick:.1f}" for tick in original_x_ticks], color=text_color)
    plt.yticks(valid_yticks, [f"{tick:.1f}" for tick in original_y_ticks], color=text_color)

    # Add labels, legend, and grid
    plt.xlabel("Playtime (hours)", color=text_color)
    plt.ylabel("Achievements Unlocked", color=text_color)
    plt.legend(facecolor=background_color, edgecolor=grid_color, labelcolor=text_color)
    plt.grid(True, linestyle="--", color=grid_color, alpha=0.5)
    plt.title("Playtime vs Achievements (Steam Theme)", color=text_color)

    # Adjust plot border colors
    ax.spines['bottom'].set_color(grid_color)
    ax.spines['left'].set_color(grid_color)
    ax.spines['top'].set_color(background_color)  # Hide top and right spines
    ax.spines['right'].set_color(background_color)

    plt.show()

def playtime_comparison(steam_id):
    user = average_playtime(steam_id) / 60
    global_time = fetch_average_playtime()
    return(user/global_time) * 100
