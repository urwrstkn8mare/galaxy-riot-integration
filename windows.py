from common import RiotPlugin
from consts import (
    GameID,
    logger,
    RIOT_CLIENT_LOCATION,
    LOL_DOWNLOAD,
    LOR_DOWNLOAD,
    VALORANT_DOWNLOAD,
    INSTALLER_PATH,
    START_MENU_FOLDER,
)
from galaxy.api.consts import LocalGameState
from galaxy.api.types import LocalGame
import os, subprocess, requests, asyncio


class WindowsRiotPlugin(RiotPlugin):
    def __init__(self, reader, writer, token):
        super().__init__(reader, writer, token)
        self._check_running_task = None
        self._check_installed_task = None
        self._running = {
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
        self._installed = {
            GameID.league_of_legends: False,
            GameID.legends_of_runeterra: False,
            GameID.valorant: False,
        }

    async def get_local_games(self):
        logger.info("Getting local games")
        out = []
        for key in self._running.keys():
            out.append(LocalGame(key, self._running[key]["status"]))
        return out

    async def uninstall_game(self, game_id):
        os.system("appwiz.cpl")

    async def launch_game(self, game_id):
        cmd = f'"{RIOT_CLIENT_LOCATION}" --launch-product={game_id} --launch-patchline=live'
        self._running[game_id]["proc"] = subprocess.Popen(cmd)

    async def install_game(self, game_id):
        logger.info("Installing game")
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
            open(INSTALLER_PATH, "wb").write(r.content)
            subprocess.Popen(INSTALLER_PATH)

    async def _check_installed(self):
        shortcuts = os.listdir(START_MENU_FOLDER)
        self._installed[GameID.league_of_legends] = (
            "League of Legends.lnk" in shortcuts
        )
        self._installed[GameID.legends_of_runeterra] = (
            "Legends of Runeterra.lnk" in shortcuts
        )
        self._installed[GameID.valorant] = "VALORANT.lnk" in shortcuts
        logger.info(f"Checked installed: {self._installed}")
        await asyncio.sleep(15)

    async def _check_running(self):
        for key in self._running.keys():
            if (
                self._running[key]["proc"] is not None
                and self._running[key]["proc"].poll() is None
                and self._running[key]["status"]
                != LocalGameState.Installed | LocalGameState.Running
            ):
                self._running[key]["status"] = (
                    LocalGameState.Installed | LocalGameState.Running
                )
                self.update_local_game_status(
                    LocalGame(
                        key, LocalGameState.Installed | LocalGameState.Running,
                    )
                )
                self.game_time_tracker.start_tracking_game(key)
            elif (
                self._running[key]["proc"] is None
                or self._running[key]["proc"].poll() is not None
            ):
                if (
                    self._running[key]["status"]
                    == LocalGameState.Installed | LocalGameState.Running
                ):
                    self.game_time_tracker.stop_tracking_game(key)

                if (
                    self._running[key]["status"] != LocalGameState.None_
                    and not self._installed[key]
                ):
                    self._running[key]["status"] = self._running[key][
                        "status"
                    ] = LocalGameState.None_
                    self.update_local_game_status(
                        LocalGame(key, LocalGameState.None_)
                    )
                elif (
                    self._running[key]["status"] != LocalGameState.Installed
                    and self._installed[key]
                ):
                    self._running[key]["status"] = self._running[key][
                        "status"
                    ] = LocalGameState.Installed
                    self.update_local_game_status(
                        LocalGame(key, LocalGameState.Installed)
                    )
        logger.info(f"Checked running: {self._running}")
        await asyncio.sleep(5)

    def tick(self):
        if self._check_running_task is None or self._check_running_task.done():
            self._check_running_task = self.create_task(
                self._check_running(), "Check Running Task"
            )
        if (
            self._check_installed_task is None
            or self._check_installed_task.done()
        ):
            self._check_installed_task = self.create_task(
                self._check_installed(), "Check Installed Task"
            )
        logger.info("Tick!")

    async def shutdown(self):
        if os.path.isfile(INSTALLER_PATH):
            os.remove(INSTALLER_PATH)
        await super().shutdown()
