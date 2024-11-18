import time
from operator import itemgetter

import requests
import datetime
from datetime import datetime

api_key = "5409DBECBF319D8375208A2EC86A66FE"
koen = "76561198030044972"
zack = "76561198055954925"
test = "76561197974698915"
test2 = "76561198285646362"



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
    for i, game in enumerate(top_games, start=1):
        print(f'Your number {i} most played game is {game["name"]} '
              f'with {game["playtime_forever"] // 60} hours.')

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



