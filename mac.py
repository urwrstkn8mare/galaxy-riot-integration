from consts import (
    logger,
    MAC_INSTALLER,
    LOL_BUNDLE_IDENTIFIER,
    GameID,
    MAC_UNINSTALLER,
)
import subprocess, os, asyncio
from galaxy.api.consts import LocalGameState
from galaxy.api.types import LocalGame


class MacLocalClient:
    def __init__(self):
        self._check_game_status_task = None
        self._get_application_location_task = None
        self._application_location = None
        self.lol_proc = None
        self.lol_status = LocalGameState.None_

    async def shutdown(self):
        pass

    async def install_game(self, game_id):
        logger.info(f"Installing: {game_id}")
        if GameID:
            subprocess.Popen(f'sh "{MAC_INSTALLER}"', shell=True)

    async def uninstall_game(self, game_id):
        logger.info(f"Uninstalling: {game_id}")
        if self.lol_installed:
            subprocess.Popen(
                f'sh "{MAC_UNINSTALLER}" "{self._application_location}"'
            )

    def _lol_is_running(self) -> bool:
        return (self.lol_proc is not None) and (self.lol_proc.poll() is None)

    async def launch_game(self, game_id):
        if not self._lol_is_running():
            logger.info(f"Launching: {game_id}")
            self.lol_proc = subprocess.Popen(
                f"open --wait-apps -b {LOL_BUNDLE_IDENTIFIER}", shell=True
            )

    @property
    def lol_installed(self) -> bool:
        return self._application_location is not None

    async def _get_application_location(self):
        cmd = f'mdfind kMDItemCFBundleIdentifier = "{LOL_BUNDLE_IDENTIFIER}"'
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as proc:
            out = proc.stdout.read().decode("ascii").split("\n")
            self._application_location = (
                None if out[0] == "" else os.path.abspath(out[0])
            )
        await asyncio.sleep(5)

    async def get_local_games(self):
        return [LocalGame(GameID.league_of_legends, self.lol_status)]

    async def _check_game_status(self, update, on_start, on_stop):
        if self._lol_is_running() and (
            self.lol_status != LocalGameState.Installed | LocalGameState.Running
        ):
            self.lol_status = LocalGameState.Installed | LocalGameState.Running
            update(
                LocalGame(
                    GameID.league_of_legends,
                    LocalGameState.Installed | LocalGameState.Running,
                )
            )
            on_start(GameID.league_of_legends)
        elif not self._lol_is_running():
            if self.lol_installed and (
                self.lol_status != LocalGameState.Installed
            ):
                self.lol_status = LocalGameState.Installed
                update(
                    LocalGame(
                        GameID.league_of_legends, LocalGameState.Installed
                    )
                )
                on_stop(GameID.league_of_legends)
            elif not self.lol_installed and (
                self.lol_status != LocalGameState.None_
            ):
                self.lol_status = LocalGameState.None_
                update(
                    LocalGame(GameID.league_of_legends, LocalGameState.None_)
                )
        await asyncio.sleep(5)

    def tick(self, update, on_start, on_stop, create_task):
        if (
            self._get_application_location_task is None
            or self._get_application_location_task.done()
        ):
            create_task(
                self._get_application_location(),
                "Get Application Location Task",
            )
        if (
            self._check_game_status_task is None
            or self._check_game_status_task.done()
        ):
            create_task(
                self._check_game_status(update, on_start, on_stop),
                "Check Game Status Task",
            )
        logger.info("Tick!")
