import json, os, winreg, logging

from yaml import load, FullLoader

from utils import misc
import consts

log = logging.getLogger(__name__)


class LocalClient:
    def __init__(self):
        self.process = dict.fromkeys(consts.GAME_IDS, None)
        self.install_location = dict.fromkeys(consts.GAME_IDS + [consts.GameID.vanguard], None)
        self.riot_client_services_path = self.get_rcs_path()

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
        p = misc.open_path(
            self.riot_client_services_path,
            [f"--launch-product={game_id}", "--launch-patchline=live"],
        )
        if save_process:
            self.process[game_id] = p
        return p

    def uninstall(self, game_id):
        misc.open_path(
            self.riot_client_services_path,
            [f"--uninstall-product={game_id}", "--uninstall-patchline=live"],
        )

    def update_installed(self):
        self.riot_client_services_path = self.get_rcs_path()

        for game_id in self.install_location.keys():
            # Vanguard should be in Program Files. I don't think its changeable.
            if game_id == consts.GameID.vanguard:
                if os.access(
                    os.path.join(consts.VANGUARD_INSTALL_LOCATION, "uninstall.exe"), os.X_OK
                ):
                    self.install_location[game_id] = consts.VANGUARD_INSTALL_LOCATION
            # Read product_install_full_path from yaml.
            else:
                try:
                    with open(misc.get_product_settings_path(game_id), "r") as file:
                        product_settings = load(file, Loader=FullLoader)
                        if "product_install_full_path" in product_settings:
                            self.install_location[game_id] = os.path.abspath(
                                product_settings["product_install_full_path"]
                            )
                        else:
                            self.install_location[game_id] = None
                except FileNotFoundError:
                    self.install_location[game_id] = None

    def get_rcs_path(self):
        try:
            with open(consts.RIOT_CLIENT_INSTALLS_PATH, "r") as file:
                client_installs = json.load(file)
                rcs_path = os.path.abspath(client_installs["rc_default"])
                if not os.access(rcs_path, os.X_OK):
                    return None
                return rcs_path
        except FileNotFoundError:
            return None
