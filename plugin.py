import sys, platform, os, requests, asyncio, subprocess, pickle, logging
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import Platform, OSCompatibility
from galaxy.api.types import (
    Authentication,
    Game,
    LicenseInfo,
    LicenseType,
    LocalGame,
    LocalGameState,
)
from galaxyutils.time_tracker import TimeTracker, GameNotTrackedException

from consts import (
    START_MENU_FOLDER,
    GameID,
    LOL_DOWNLOAD,
    LOR_DOWNLOAD,
    VALORANT_DOWNLOAD,
    LOCAL_FILE_CACHE,
    GAME_TIME_CACHE_KEY,
    INSTALLER_PATH,
    RIOT_CLIENT_LOCATION,
)

logger = logging.getLogger(__name__)


def is_windows():
    return platform.system().lower() == "windows"


class RiotPlugin(Plugin):
    def __init__(self, reader, writer, token):
        super().__init__(
            Platform.RiotGames,  # choose platform from available list
            "0.1.1",  # version
            reader,
            writer,
            token,
        )
        self._check_running_task = None
        self._check_installed_task = None
        self.game_time_cache = None
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

    async def authenticate(self, stored_credentials=None):
        self.store_credentials({"dummy": "dummy"})
        return (
            Authentication("riot_user", "Riot User")
            if is_windows()
            else Authentication()
        )

    async def get_owned_games(self):
        logger.info("Getting owned games")
        return [
            Game(
                GameID.league_of_legends,
                "League of Legends",
                None,
                LicenseInfo(LicenseType.FreeToPlay),
            ),
            Game(
                GameID.legends_of_runeterra,
                "Legends of Runeterra",
                None,
                LicenseInfo(LicenseType.FreeToPlay),
            ),
            Game(
                GameID.valorant,
                "Valorant",
                None,
                LicenseInfo(LicenseType.FreeToPlay),
            ),
        ]

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

    async def get_os_compatibility(self, game_id, context):
        logger.info("Getting os compatibility")
        if game_id == GameID.league_of_legends:
            return OSCompatibility.Windows | OSCompatibility.MacOS
        elif game_id == GameID.legends_of_runeterra:
            return OSCompatibility.Windows
        elif game_id == GameID.valorant:
            return OSCompatibility.Windows
        else:
            return

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
            with open(INSTALLER_PATH, "wb") as f:
                f.write(r.content)
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

    def handshake_complete(self):
        if GAME_TIME_CACHE_KEY in self.persistent_cache:
            self.game_time_cache = pickle.loads(
                bytes.fromhex(self.persistent_cache[GAME_TIME_CACHE_KEY])
            )
        else:
            try:
                file = open(LOCAL_FILE_CACHE, "r")
                for line in file.readlines():
                    if line[:1] != "#":
                        self.game_time_cache = pickle.loads(bytes.fromhex(line))
                        break
                file.close()
            except FileNotFoundError:
                self.game_time_tracker = TimeTracker()
                return
        self.game_time_tracker = TimeTracker(
            game_time_cache=self.game_time_cache
        )

    def game_times_import_complete(self):
        self.game_time_cache = self.game_time_tracker.get_time_cache_hex()
        self.persistent_cache[
            GAME_TIME_CACHE_KEY
        ] = self.game_time_tracker.get_time_cache_hex()
        self.push_cache()

    async def shutdown(self):
        if os.path.exists(INSTALLER_PATH):
            os.remove(INSTALLER_PATH)
        if self.game_time_cache:
            file = open(LOCAL_FILE_CACHE, "w+")
            file.write("# DO NOT EDIT THIS FILE (pretty pls)\n")
            file.write(self.game_time_tracker.get_time_cache_hex())
            file.close()
        await super().shutdown()

    async def get_game_time(self, game_id, context):
        try:
            time = self.game_time_tracker.get_tracked_time(game_id)
        except GameNotTrackedException:
            time = None
        return time


def main():
    create_and_run_plugin(RiotPlugin, sys.argv)


if __name__ == "__main__":
    main()
