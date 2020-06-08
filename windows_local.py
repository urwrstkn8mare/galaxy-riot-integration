import os, subprocess, requests
from galaxy.api.types import LocalGameState, LocalGame
from consts import (
    GameID,
    RIOT_CLIENT_LOCATION,
    LOL_DOWNLOAD,
    LOR_DOWNLOAD,
    VALORANT_DOWNLOAD,
    INSTALLER_PATH,
    START_MENU_FOLDER,
)


class WindowsLocalClient:
    def __init__(self):
        self.running = {
            GameID.league_of_legends: {
                "proc": None,
                "status": LocalGameState.None_,
            },
            GameID.legends_of_runeterra: {
                "proc": None,
                "status": LocalGameState.None_,
            },
            GameID.valorant: {"proc": None, "status": LocalGameState.None_},
        }
        self.installed = {
            GameID.league_of_legends: False,
            GameID.legends_of_runeterra: False,
            GameID.valorant: False,
        }

    def get_local_games(self):
        out = []
        for key in self.running.keys():
            out.append(LocalGame(key, self.running[key]["status"]))
        return out

    def uninstall_game(self, game_id):
        os.system("appwiz.cpl")

    def launch_game(self, game_id):
        cmd = f'"{RIOT_CLIENT_LOCATION}" --launch-product={game_id} --launch-patchline=live'
        self.running[game_id]["proc"] = subprocess.Popen(cmd)

    def install_game(self, game_id):
        if os.path.exists(RIOT_CLIENT_LOCATION):
            subprocess.Popen(
                f'"{RIOT_CLIENT_LOCATION}" --launch-product={game_id} --launch-patchline=live'
            )
        else:
            url = ""
            if game_id == GameID.league_of_legends:
                url = LOL_DOWNLOAD
            elif game_id == GameID.legends_of_runeterra:
                url = LOR_DOWNLOAD
            elif game_id == GameID.valorant:
                url = VALORANT_DOWNLOAD
            r = requests.get(url, allow_redirects=True)
            with open(INSTALLER_PATH, "wb") as f:
                f.write(r.content)
            subprocess.Popen(INSTALLER_PATH)

    def check_installed(self):
        shortcuts = os.listdir(START_MENU_FOLDER)
        self.installed[GameID.league_of_legends] = (
            "League of Legends.lnk" in shortcuts
        )
        self.installed[GameID.legends_of_runeterra] = (
            "Legends of Runeterra.lnk" in shortcuts
        )
        self.installed[GameID.valorant] = "VALORANT.lnk" in shortcuts

    def check_running(self, on_start, on_stop, update):
        for key in self.running.keys():
            if (
                self.running[key]["proc"] is not None
                and self.running[key]["proc"].poll() is None
                and self.running[key]["status"]
                != LocalGameState.Installed | LocalGameState.Running
            ):
                self.running[key]["status"] = (
                    LocalGameState.Installed | LocalGameState.Running
                )
                update(
                    LocalGame(
                        key, LocalGameState.Installed | LocalGameState.Running,
                    )
                )
                # self.game_time_tracker.start_tracking_game(key)
                on_start(key)
            elif (
                self.running[key]["proc"] is None
                or self.running[key]["proc"].poll() is not None
            ):
                if (
                    self.running[key]["status"]
                    == LocalGameState.Installed | LocalGameState.Running
                ):
                    # self.game_time_tracker.stop_tracking_game(key)
                    on_stop(key)

                if (
                    self.running[key]["status"] != LocalGameState.None_
                    and not self.installed[key]
                ):
                    self.running[key]["status"] = self.running[key][
                        "status"
                    ] = LocalGameState.None_
                    update(LocalGame(key, LocalGameState.None_))
                elif (
                    self.running[key]["status"] != LocalGameState.Installed
                    and self.installed[key]
                ):
                    self.running[key]["status"] = self.running[key][
                        "status"
                    ] = LocalGameState.Installed
                    update(LocalGame(key, LocalGameState.Installed))

    def on_shutdown(self):
        if os.path.exists(INSTALLER_PATH):
            os.remove(INSTALLER_PATH)
