import winreg

import os

from consts import (
    GameID,
    GAME_IDS,
    REGISTRY_START_PATHS,
    SOFTWARE_PATHS,
    UNINSTALL_REGISTRY_PATH,
    GAME_REGISTY_PATH,
    UNINSTALL_STRING_KEY,
    INSTALL_LOCATION_KEY,
)
import utils


class LocalClient:
    def __init__(self):
        self.process = dict.fromkeys(GAME_IDS, None)
        self.install_location = dict.fromkeys(list(GAME_REGISTY_PATH.keys()), None)
        self.riot_client_services_path = None
        self._vangaurd_uninstall_path = None

    def game_running(self, game_id) -> bool:
        rp = self.process[game_id]  # Just an alias
        if rp is not None and rp.poll() is None:
            return True
        elif rp is not None and not rp.poll() is not None:
            # Can't use rp alias as it won't update the dict.
            self.process[game_id] = None
        return False

    def game_installed(self, game_id):
        return self.install_location[game_id] is not None

    def launch(self, game_id, *, save_process=True):
        p = utils.open_path(
            self.riot_client_services_path,
            [f"--launch-product={game_id}", "--launch-patchline=live"],
        )
        if save_process:
            self.process[game_id] = p
        return p

    def uninstall(self, game_id):
        utils.open_path(
            self.riot_client_services_path,
            [f"--uninstall-product={game_id}", "--uninstall-patchline=live"],
        )

    def update_installed(self):
        def get_riot_client_services_path_from_cmd(cmd):
            pth = ""
            found_char = False
            for char in cmd.strip():
                if char == '"':
                    if found_char:
                        break
                    else:
                        found_char = True
                elif found_char:
                    pth += char
            return pth

        games = list(GAME_REGISTY_PATH.keys())
        if self.riot_client_services_path is not None and not os.path.isfile(
            self.riot_client_services_path
        ):
            self.riot_client_services_path = None
        self._vangaurd_uninstall_path = None
        for start_path in REGISTRY_START_PATHS:
            for software_path in SOFTWARE_PATHS:
                for game_id in games.copy():
                    try:
                        reg = winreg.ConnectRegistry(None, start_path)
                        with winreg.OpenKey(
                            reg,
                            software_path + UNINSTALL_REGISTRY_PATH + GAME_REGISTY_PATH[game_id],
                        ) as key:
                            if (
                                game_id != GameID.vanguard
                                and self.riot_client_services_path is None
                            ):
                                path = get_riot_client_services_path_from_cmd(
                                    winreg.QueryValueEx(key, UNINSTALL_STRING_KEY)[0]
                                )
                                if not os.path.isfile(path):
                                    path = None
                                self.riot_client_services_path = path
                            elif game_id == GameID.vanguard:
                                self._vangaurd_uninstall_path = os.path.abspath(
                                    winreg.QueryValueEx(key, UNINSTALL_STRING_KEY)[0].strip('"')
                                )
                            self.install_location[game_id] = os.path.abspath(
                                winreg.QueryValueEx(key, INSTALL_LOCATION_KEY)[0]
                            )
                    except OSError:
                        continue
                    else:
                        games.remove(game_id)
        for game_id in games:
            self.install_location[game_id] = None
