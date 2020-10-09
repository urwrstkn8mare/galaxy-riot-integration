import os, asyncio, logging, subprocess, tempfile

import requests

from consts import LOCAL_FILE_CACHE

log = logging.getLogger(__name__)


async def get_size_at_path(start_path, *, if_none=None):
    if start_path is None:
        return if_none
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            await asyncio.sleep(0)
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    log.debug(f"Size: {total_size} bytes - {start_path}")
    return total_size  # in bytes

def get_product_settings_path(game_id):
    # Given the game ID, returns the path of the product settings yaml file.
    return os.path.expandvars("%PROGRAMDATA%\\Riot Games\\Metadata\\{0}.live\\{0}.live.product_settings.yaml".format(game_id))

def get_riot_client_installs_path():
    # Returns the path of the Riot Client settings yaml file.
    return os.path.expandvars("%PROGRAMDATA%\\Riot Games\\RiotClientInstalls.json")

def run(cmd, *, shell=False):
    log.info(f"Running: {cmd}")
    return subprocess.Popen(cmd, shell=shell)


def open_path(path, args=[]):
    cmd = f'"{path}" {" ".join(args)}'.strip()
    log.info(f"Opening: {path}\nWith args: {args}")
    return run(cmd)


def download(url) -> str:
    log.info(f"Downloading: {url}")
    r = requests.get(url)
    download_path = os.path.join(tempfile.gettempdir(), url.split("/")[-1])
    with open(download_path, "wb") as f:
        f.write(r.content)
    return download_path


def cleanup():  # Clean up files created by/for earlier version of the plugin not needed anymore
    old_riot_client_location_file = os.path.expandvars(
        "%LOCALAPPDATA%\\GOG.com\\Galaxy\\plugins\\installed\\riot_client_location.txt"
    )
    old_installer_path = os.path.abspath(
        os.path.join(os.path.abspath(__file__), "..", "..", "riot_installer.exe")
    )
    old_delete_paths = [old_riot_client_location_file, old_installer_path]
    old_local_file_cache = os.path.abspath(
        os.path.join(os.path.abspath(__file__), "..", "..", "play_time_cache.txt")
    )  # don't delete just rename
    for path in old_delete_paths:
        if os.path.isfile(path):
            os.remove(path)
    if os.path.isfile(old_local_file_cache):
        os.rename(old_local_file_cache, LOCAL_FILE_CACHE)
