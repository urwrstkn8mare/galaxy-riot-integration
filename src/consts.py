import os, logging

logger = logging.getLogger(__name__)

RIOT_CLIENT_LOCATION = "C:\\Riot Games\\Riot Client\\RiotClientServices.exe"
RIOT_CLIENT_LOCATION_FILE = os.path.expandvars(
    "%LOCALAPPDATA%\\GOG.com\\Galaxy\\plugins\\installed\\riot_client_location.txt"
)
START_MENU_FOLDER = (
    "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Riot Games"
)
LOL_DOWNLOAD = "https://lol.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.na.exe"
LOR_DOWNLOAD = "https://bacon.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.exe"
VALORANT_DOWNLOAD = "https://valorant.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.live.eu.exe"
LOCAL_FILE_CACHE = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "..", "..", "play_time_cache.txt")
)
GAME_TIME_CACHE_KEY = "game_time_cache"
INSTALLER_PATH = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "..", "..", "riot_installer.exe")
)


class GameID:
    league_of_legends = "league_of_legends"
    legends_of_runeterra = "bacon"
    valorant = "valorant"


if os.path.isfile(RIOT_CLIENT_LOCATION_FILE):
    with open(RIOT_CLIENT_LOCATION_FILE) as f:
        path = os.path.abspath(f.readline().strip().strip('"'))
        RIOT_CLIENT_LOCATION = (
            path
            if "RiotClientServices.exe" in path
            else os.path.join(path, "RiotClientServices.exe",)
        )
logger.info("RIOT_CLIENT_LOCATION: %s", RIOT_CLIENT_LOCATION)
