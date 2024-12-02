from operator import itemgetter
import requests
import datetime
from datetime import datetime

api_key = "5409DBECBF319D8375208A2EC86A66FE"
koen = "76561198030044972"
zack = "76561198055954925"
test = "76561197974698915"



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
    played_games = sorted(response['response']['games'],key=itemgetter('playtime_forever'), reverse=True)
    return played_games

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

