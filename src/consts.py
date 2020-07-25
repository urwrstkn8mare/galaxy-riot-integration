import os, winreg


class GameID:
    league_of_legends = "league_of_legends"
    legends_of_runeterra = "bacon"
    valorant = "valorant"
    vanguard = "vanguard"  # not really a game


GAME_IDS = [GameID.legends_of_runeterra, GameID.league_of_legends, GameID.valorant]
REGISTRY_START_PATHS = [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]
SOFTWARE_PATHS = ["SOFTWARE\\", "SOFTWARE\\WOW6432Node\\"]
UNINSTALL_REGISTRY_PATH = "Microsoft\\Windows\\CurrentVersion\\Uninstall\\"
GAME_REGISTY_PATH = {
    GameID.league_of_legends: "Riot Game league_of_legends.live",
    GameID.legends_of_runeterra: "Riot Game bacon.live",
    GameID.valorant: "Riot Game valorant.live",
    "vanguard": "Riot Vanguard",
}
UNINSTALL_STRING_KEY = "UninstallString"
INSTALL_LOCATION_KEY = "InstallLocation"
DOWNLOAD_URL = {
    GameID.league_of_legends: "https://lol.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.na.exe",  # noqa: E501
    GameID.legends_of_runeterra: "https://bacon.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.exe",  # noqa: E501
    GameID.valorant: "https://valorant.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.live.eu.exe",  # noqa: E501
}
LOCAL_FILE_CACHE = os.path.expandvars(
    "%LOCALAPPDATA%\\GOG.com\\Galaxy\\plugins\\installed\\riot_play_time_cache.txt"
)
