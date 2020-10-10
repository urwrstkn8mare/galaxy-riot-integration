import json, os, winreg

from yaml import load, FullLoader

import utils.misc
from consts import (
    GameID,
    GAME_IDS,
    REGISTRY_START_PATHS,
    SOFTWARE_PATHS,
    UNINSTALL_REGISTRY_PATH,
    GAME_REGISTRY_PATH,
    UNINSTALL_STRING_KEY,
    INSTALL_LOCATION_KEY,
)


class LocalClient:
    def __init__(self):
        self.process = dict.fromkeys(GAME_IDS, None)
        self.install_location = dict.fromkeys(
            list(GAME_REGISTRY_PATH.keys()), None)
        self.riot_client_services_path = self.get_rcs_path()
        if not os.path.isfile(self.riot_client_services_path):
            self.riot_client_services_path = None
        self._vanguard_uninstall_path = None

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
        p = utils.misc.open_path(
            self.riot_client_services_path,
            [f"--launch-product={game_id}", "--launch-patchline=live"],
        )
        if save_process:
            self.process[game_id] = p
        return p

    def uninstall(self, game_id):
        utils.misc.open_path(
            self.riot_client_services_path,
            [f"--uninstall-product={game_id}", "--uninstall-patchline=live"],
        )

    def update_installed(self):
        if self.riot_client_services_path == None:
            self.riot_client_services_path = self.get_rcs_path()
        self._vanguard_uninstall_path = None

        for game_id in GAME_IDS:
            # Vanguard doesn't have a settings.yaml file. Need to use old registry method.
            if game_id == GameID.vanguard:
                for start_path in REGISTRY_START_PATHS:
                    for software_path in SOFTWARE_PATHS:
                        try:
                            reg = winreg.ConnectRegistry(None, start_path)
                            with winreg.OpenKey(reg, software_path + UNINSTALL_REGISTRY_PATH + GAME_REGISTRY_PATH[game_id]) as key:
                                self._vanguard_uninstall_path = os.path.abspath(
                                    winreg.QueryValueEx(key, UNINSTALL_STRING_KEY)[0].strip('"'))
                        except OSError:
                            log.error(OSError)
                            continue
            # Read product_install_full_path from yaml.
            else:
                try:
                    with open(utils.misc.get_product_settings_path(game_id), 'r') as file:
                        product_settings = load(file, Loader=FullLoader)
                        install_path = product_settings['product_install_full_path']
                        self.install_location[game_id] = os.path.abspath(
                            install_path)
                except:
                    self.install_location[game_id] = None

    def get_rcs_path(self):
        try:
            with open(utils.misc.get_riot_client_installs_path(), 'r') as file:
                client_installs = json.load(file)
                rcs_path = os.path.abspath(client_installs['rc_default'])
        except:
            rcs_path = None
            pass
        return rcs_path