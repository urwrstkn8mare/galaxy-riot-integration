import sys, platform, logging, os
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.consts import Platform
from galaxy.api.types import Authentication, Game, LicenseInfo, LicenseType

from const import WIN_INSTALL_LOCATION

logger = logging.getLogger(__name__)
logger.info(WIN_INSTALL_LOCATION)


def is_windows():
    return platform.system().lower() == "windows"


class RiotPlugin(Plugin):
    def __init__(self, reader, writer, token):
        super().__init__(
            Platform.Test,  # choose platform from available list
            "0.1",  # version
            reader,
            writer,
            token,
        )

    # implement methods

    # required
    async def authenticate(self, stored_credentials=None):
        return (
            Authentication("windows", "Windows")
            if is_windows()
            else Authentication()
        )

    # required
    async def get_owned_games(self):
        return [
            Game(
                "riot.legends",
                "League of Legends",
                None,
                LicenseInfo(LicenseType.FreeToPlay),
            ),
            Game(
                "riot.runterra",
                "Legends of Runeterra",
                None,
                LicenseInfo(LicenseType.FreeToPlay),
            ),
            Game(
                "riot.valorant",
                "Valorant",
                None,
                LicenseInfo(LicenseType.FreeToPlay),
            ),
        ]

    async def uninstall_game(self, game_id):
        os.system("appwiz.cpl")

    # async def get_local_games(self):
    #     local_games = []
    #     for


def main():
    create_and_run_plugin(RiotPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()
