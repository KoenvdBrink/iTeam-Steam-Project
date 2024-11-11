from operator import itemgetter

import requests
import datetime
from datetime import datetime

api_key = "5409DBECBF319D8375208A2EC86A66FE"
koen = "76561198030044972"
zack = "76561198055954925"



def get_player_summ(steam_id):
    """
    Returns basic profile information for a list of 64-bit Steam IDs.
    https://developer.valvesoftware.com/wiki/Steam_Web_API#GetGlobalAchievementPercentagesForApp_.28v0001.29
    for detailed information about returned dictionary contents.
    :param steam_id: int
    :return: Dict
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

    :param steam_id:
    :return:
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
    Gives the date the user last logged off on steam.
    :param steam_id: int
    :return: str
    """
    time_unix = get_player_summ(steam_id)['response']['players'][0]['lastlogoff']
    return datetime.fromtimestamp(time_unix)


def offline_for(steam_id):
    """
    calculates the amount of hours it has been since the user last logged off on steam.
    rounds down to the nearest full hour.
    returns -1 of the user is online
    :param steam_id: int
    :return: float/int
    """
    now = datetime.now()
    then = last_logged_off(steam_id)
    if get_player_summ(steam_id)['response']['players'][0]['personastate'] != 0:
        return -1
    else:
        return abs(divmod((now - then).total_seconds(),3600)[0])

def most_played_games(steam_id):
    """

    :param steam_id:
    :return:
    """
    played_games = get_owned_games(steam_id)
    for i in range(5):
        print(f'Your number {i+1} most played game is {played_games[i]['name']} '
              f'with {played_games[i]['playtime_forever']//60} hours.')