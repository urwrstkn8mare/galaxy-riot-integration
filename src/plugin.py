import sys, asyncio, pickle, logging, os

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


from consts import GameID, DOWNLOAD_URL, GAME_IDS, LOCAL_FILE_CACHE
from local import LocalClient
from utils import misc, time_tracker
from version import __version__

log = logging.getLogger(__name__)


class RiotPlugin(Plugin):
    def __init__(self, reader, writer, token):
        super().__init__(
            Platform.RiotGames,  # choose platform from available list
            __version__,  # version
            reader,
            writer,
            token,
        )
        self.local_client = LocalClient()
        self.status = dict.fromkeys(GAME_IDS, LocalGameState.None_)
        self._update_task = None

    async def authenticate(self, stored_credentials=None):
        self.store_credentials({"dummy": "dummy"})
        return Authentication("riot_user", "Riot User")

    async def get_owned_games(self):
        log.info("Getting owned games")
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
        log.info("Getting local games")
        local_games = []
        for game_id in GAME_IDS:
            if self.local_client.game_installed(game_id):
                local_game = LocalGame(game_id, LocalGameState.Installed)
                local_games.append(local_game)
        log.debug(f"RIOT_INSTALLED_GAMES: {local_games}")
        return local_games

    async def prepare_local_size_context(self, game_ids):
        sizes = []
        for game_id in GAME_IDS:
            size = await misc.get_size_at_path(
                self.local_client.install_location[game_id], if_none=0
            )
            if game_id == GameID.valorant:
                size += await misc.get_size_at_path(
                    self.local_client.install_location[GameID.vanguard], if_none=0
                )
            if size == 0:
                size = None
            sizes.append(size)
        return dict(zip(game_ids, sizes))

    async def get_local_size(self, game_id: str, context):
        return context[game_id]

    async def uninstall_game(self, game_id):
        self.local_client.update_installed()
        self.local_client.uninstall(game_id)

    async def launch_game(self, game_id):
        log.debug("RCS location: " + self.local_client.riot_client_services_path)
        self.local_client.update_installed()
        self.local_client.launch(game_id)

    async def get_os_compatibility(self, game_id, context):
        log.info("Getting os compatibility")
        if game_id == GameID.league_of_legends:
            return OSCompatibility.Windows | OSCompatibility.MacOS
        elif game_id == GameID.legends_of_runeterra:
            return OSCompatibility.Windows
        elif game_id == GameID.valorant:
            return OSCompatibility.Windows

    async def install_game(self, game_id):
        log.info("Installing game")
        self.local_client.update_installed()
        if self.local_client.riot_client_services_path is None:
            misc.download(DOWNLOAD_URL[game_id], misc.open_path)
        else:
            self.local_client.launch(game_id, save_process=False)

    async def _update(self):
        def update(game_id, status: LocalGameState):
            if self.status[game_id] != status:
                self.status[game_id] = status
                self.update_local_game_status(LocalGame(game_id, status))
                log.info(f"Updated {game_id} to {status}")
                return True  # return true if needed to update
            return False

        self.local_client.update_installed()
        for game_id in GAME_IDS:
            if self.local_client.game_running(game_id):
                if update(game_id, LocalGameState.Installed | LocalGameState.Running):
                    self.game_time_tracker.start_tracking_game(game_id)
            elif self.local_client.game_installed(game_id):
                if update(game_id, LocalGameState.Installed):
                    if game_id in self.game_time_tracker.get_tracking_games():
                        self.game_time_tracker.stop_tracking_game(game_id)
            else:
                update(game_id, LocalGameState.None_)

        log.debug(f"self.local_client.install_location: {self.local_client.install_location}")
        log.debug(f"self.status: {self.status}")

        await asyncio.sleep(5)

    def tick(self):
        if self._update_task is None or self._update_task.done():
            self._update_task = self.create_task(self._update(), "Update Task")

    # Time Tracker

    async def get_game_time(self, game_id, context):
        try:
            return self.game_time_tracker.get_tracked_time(game_id)
        except time_tracker.GameNotTrackedException:
            return None

    def handshake_complete(self):
        misc.cleanup()

        self.game_time_cache = None
        if "game_time_cache" in self.persistent_cache:
            self.game_time_cache = pickle.loads(
                bytes.fromhex(self.persistent_cache["game_time_cache"])
            )
        else:
            if os.path.isfile(LOCAL_FILE_CACHE):
                with open(LOCAL_FILE_CACHE, "r") as file:
                    for line in file.readlines():
                        if line[:1] != "#":
                            self.game_time_cache = pickle.loads(bytes.fromhex(line))
                            break

        self.game_time_tracker = time_tracker.TimeTracker(game_time_cache=self.game_time_cache)

    async def shutdown(self):
        misc.kill_all_processes()
        for game_id in self.game_time_tracker.get_tracking_games():
            self.game_time_tracker.stop_tracking_game(game_id)
        if self.game_time_cache is not None:
            with open(LOCAL_FILE_CACHE, "w+") as file:
                file.write("# DO NOT EDIT THIS FILE\n")
                file.write(self.game_time_tracker.get_time_cache_hex())
                log.info("Wrote to local file cache")
        await super().shutdown()

    def game_times_import_complete(self):
        if len(self.game_time_tracker.get_tracking_games()) > 0:
            log.debug("Game time still being tracked. Not setting cache yet.")
        else:
            self.game_time_cache = self.game_time_tracker.get_time_cache()
            log.debug(f"game_time_cache: {self.game_time_cache}")
            self.persistent_cache["game_time_cache"] = self.game_time_tracker.get_time_cache_hex()
            self.push_cache()


def main():
    create_and_run_plugin(RiotPlugin, sys.argv)


if __name__ == "__main__":
    main()
