from galaxy.api.consts import LocalGameState
from galaxy.api.types import LocalGame
import os, subprocess, requests, asyncio
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


class WindowsLocalClient:
    def __init__(self):
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
        logger.info("Getting local games...")
        out = []
        for key in self._running.keys():
            out.append(LocalGame(key, self._running[key]["status"]))
        logger.info(f"Got local games: {out}")
        return out

    async def uninstall_game(self, game_id):
        logger.info(f"Uninstalling: {game_id}")
        os.system("appwiz.cpl")

    async def launch_game(self, game_id):
        logger.info(f"Launching: {game_id}")
        cmd = f'"{RIOT_CLIENT_LOCATION}" --launch-product={game_id} --launch-patchline=live'
        self._running[game_id]["proc"] = subprocess.Popen(cmd)

    async def install_game(self, game_id):
        logger.info(f"Installing {game_id}")
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

    def _game_is_running(self, game_id) -> bool:
        return (
            self._running[game_id]["proc"] is not None
            and self._running[game_id]["proc"] is None
        )

    async def _check_running(self, update, on_start, on_stop):
        for key in self._running.keys():
            if self._game_is_running(key) and (
                self._running[key]["status"]
                != LocalGameState.Installed | LocalGameState.Running
            ):
                self._running[key]["status"] = (
                    LocalGameState.Installed | LocalGameState.Running
                )
                update(
                    LocalGame(
                        key, LocalGameState.Installed | LocalGameState.Running,
                    )
                )
                on_start(key)
            elif not self._game_is_running(key):
                if self._installed[key] and (
                    self._running[key]["status"] != LocalGameState.Installed
                ):
                    self._running[key]["status"] = LocalGameState.Installed
                    update(LocalGame(key, LocalGameState.Installed))
                    on_stop(key)
                elif not self._installed[key] and (
                    self._running[key]["status"] != LocalGameState.None_
                ):
                    self._running[key]["status"] = LocalGameState.None_
                    update(LocalGame(key, LocalGameState.None_))
        logger.info(f"Checked running: {self._running}")
        await asyncio.sleep(5)

    def tick(self, update, on_start, on_stop, create_task):
        if self._check_running_task is None or self._check_running_task.done():
            self._check_running_task = create_task(
                self._check_running(update, on_start, on_stop),
                "Check Running Task",
            )
        if (
            self._check_installed_task is None
            or self._check_installed_task.done()
        ):
            self._check_installed_task = create_task(
                self._check_installed(), "Check Installed Task"
            )
        logger.info("Tick!")

    async def shutdown(self):
        if os.path.isfile(INSTALLER_PATH):
            os.remove(INSTALLER_PATH)
