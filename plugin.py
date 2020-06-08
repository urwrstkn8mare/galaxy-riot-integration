import sys, platform, asyncio, pickle, logging
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import Platform, OSCompatibility
from galaxy.api.types import (
    Authentication,
    Game,
    LicenseInfo,
    LicenseType,
)
from galaxyutils.time_tracker import TimeTracker, GameNotTrackedException

from consts import (
    GameID,
    LOCAL_FILE_CACHE,
    GAME_TIME_CACHE_KEY,
)
from windows_local import WindowsLocalClient

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
        self._local_client = WindowsLocalClient()

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

    async def get_os_compatibility(self, game_id, context):
        logger.info("Getting OS compatibility")
        if game_id == GameID.league_of_legends:
            return OSCompatibility.Windows | OSCompatibility.MacOS
        elif game_id == GameID.legends_of_runeterra:
            return OSCompatibility.Windows
        elif game_id == GameID.valorant:
            return OSCompatibility.Windows

    async def get_local_games(self):
        logger.info("Getting local games")
        return self._local_client.get_local_games()

    async def uninstall_game(self, game_id):
        logger.info(f"Uninstalling: {game_id}")
        self._local_client.uninstall_game(game_id)

    async def launch_game(self, game_id):
        logger.info(f"Launching {game_id}")
        self._local_client.launch_game(game_id)

    async def install_game(self, game_id):
        logger.info(f"Installing: {game_id}")
        self._local_client.install_game(game_id)

    async def _check_installed(self):
        self._local_client.check_installed()
        logger.info(f"Checked installed: {self._local_client.installed}")
        await asyncio.sleep(15)

    async def _check_running(self):
        self._local_client.check_running(
            self.game_time_tracker.start_tracking_game,
            self.game_time_tracker.stop_tracking_game,
            self.update_local_game_status,
        )
        logger.info(f"Checked running: {self._local_client.running}")
        await asyncio.sleep(5)

    def tick(self):
        logger.info("Tick!")
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

    def handshake_complete(self):
        logger.info("Handshake Complete")
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
        logger.info("Game times import complete")
        self.game_time_cache = self.game_time_tracker.get_time_cache_hex()
        self.persistent_cache[
            GAME_TIME_CACHE_KEY
        ] = self.game_time_tracker.get_time_cache_hex()
        self.push_cache()

    async def shutdown(self):
        logger.info("Riot Plugin shutting down")
        self._local_client.on_shutdown()
        if self.game_time_cache:
            file = open(LOCAL_FILE_CACHE, "w+")
            file.write("# DO NOT EDIT THIS FILE (pretty pls)\n")
            file.write(self.game_time_tracker.get_time_cache_hex())
            file.close()
        await super().shutdown()

    async def get_game_time(self, game_id, context):
        logger.info(f"Getting game time: {game_id}")
        try:
            time = self.game_time_tracker.get_tracked_time(game_id)
        except GameNotTrackedException:
            time = None
        return time


def main():
    create_and_run_plugin(RiotPlugin, sys.argv)


if __name__ == "__main__":
    main()
