import requests
import time
import urllib3
from modules.errors.errors import ParamError

def fetch_steam_data(api_key, steam_id):
    if not api_key or not steam_id:
        raise ParamError("Missing api_key or steam_id")
        
    # 禁用 urllib3 的不安全请求警告
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    start_time = time.time()
    
    try:
        urla = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={api_key}&steamid={steam_id}&format=json"
        urlb = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
        urlc = f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v0001/?key={api_key}&steamid={steam_id}&format=json"
        urld = f"https://api.steampowered.com/isteamuser/GetPlayerSummaries/v2/?key={api_key}&steamids={steam_id}&format=json"
        
        responsea = requests.get(urla, verify=False, timeout=10)
        dataa = responsea.json()
        
        # 频率限制
        time.sleep(0.3)
        
        responseb = requests.get(urlb, verify=False, timeout=10)
        datab = responseb.json()

        responsec = requests.get(urlc, verify=False, timeout=10)
        datac = responsec.json()
        
        responsed = requests.get(urld, verify=False, timeout=10)
        datad = responsed.json()

        # 提取数据
        steam_level = datac.get("response", {}).get("player_level", 0)
        players = datad.get("response", {}).get("players", [])
        if not players:
            raise ParamError("Player not found")
        player_data = players[0]
        
        last_logoff = time.strftime("%Y-%m-%d %H:%M", time.localtime(player_data.get("lastlogoff", 0)))

        total_playtime = 0
        games = datab.get("response", {}).get("games", [])
        for game in games:
            total_playtime += game.get("playtime_forever", 0)

        total_playtime_hours = round(total_playtime / 60.0, 1)
        game_count = datab.get("response", {}).get("game_count", 0)

        recent_games_list = dataa.get("response", {}).get("games", [])
        recent_game_names = []
        for game in recent_games_list:
            playtime_2weeks = game.get('playtime_2weeks', 0)
            playtime_2weeks_hours = round(playtime_2weeks / 60, 1)
            recent_game_names.append(f"{game['name']}({playtime_2weeks_hours} h)")

        return {
            "total_playtime_hours": total_playtime_hours,
            "game_count": game_count,
            "recent_game_count": len(recent_games_list),
            "recent_game_names": recent_game_names,
            "steam_level": steam_level,
            "nickname": player_data.get("personaname", "Unknown"),
            "last_logoff": last_logoff
        }
    except Exception as e:
        raise ParamError(f"Error fetching Steam data: {str(e)}")
