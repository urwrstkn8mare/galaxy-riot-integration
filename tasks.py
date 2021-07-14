# Desc:     Some tasks to be used by invoke that assists in
#           developing/releasing GOG Galaxy integrations.
# Usage:    1. Run 'pip install -r requirements/dev.txt'
#           2. Use 'inv pack' to build releases
#                  'inv install' to install integration to local GOG Galaxy
#                  'inv hotfix' to just overwrite the python files in the install directory.
# Source:   Slightly modified from https://github.com/tauqua/gog-galaxy-itch.io/blob/master/tasks.py
#           If you go down the rabbit hole of 'taken
#           froms', you'll find it's orginated at
#           https://github.com/bartok765/galaxy_blizzard_plugin/blob/master/tasks.py


import os
import sys
import json
import tempfile
from shutil import rmtree
from distutils.dir_util import copy_tree

from invoke import task
from galaxy.tools import zip_folder_to_file
import colorama

colorama.init()


with open(os.path.join("src", "manifest.json"), "r") as f:
    MANIFEST = json.load(f)

if sys.platform == "win32":
    DIST_DIR = os.environ["localappdata"] + "\\GOG.com\\Galaxy\\plugins\\installed"
    PIP_PLATFORM = "win32"
elif sys.platform == "darwin":
    DIST_DIR = os.path.realpath(
        "~/Library/Application Support/GOG.com/Galaxy/plugins/installed"
    )
    PIP_PLATFORM = "macosx_10_13_x86_64"
    # @see https://github.com/FriendsOfGalaxy/galaxy-integrations-updater/blob/master/scripts.py

RELEASE_DIR = "releases"


def print_task(string):
    print(colorama.Fore.CYAN + string)
    print(colorama.Style.RESET_ALL)


@task
def build(c, output="build", ziparchive=None):
    if os.path.exists(output):
        print_task("--> Removing {} directory".format(output))
        rmtree(output)

    # Firstly dependencies needs to be "flatten" with pip-compile
    # as pip requires --no-deps if --platform is used
    print_task(
        "--> Flattening dependencies to temporary requirements file from Pipfile"
    )
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        c.run("pipenv lock -r", out_stream=tmp)

    # Then install all stuff with pip to output folder
    print_task("--> Installing with pip for specific version")
    args = [
        "pip",
        "install",
        "-r",
        tmp.name,
        "--python-version",
        "37",
        "--platform",
        PIP_PLATFORM,
        '--target "{}"'.format(output),
        "--no-compile",
        "--no-deps",
        "--implementation",
        "cp",
    ]
    c.run(" ".join(args), echo=True)
    os.unlink(tmp.name)

    print_task("--> Copying source files")
    copy_tree("src", output)

    if ziparchive is not None:
        print_task("--> Compressing to {}".format(ziparchive))
        zip_folder_to_file(output, ziparchive)


@task
def hotfix(c):
    # This just overwrites the python files in the install directory. Useful if the
    # plugin has crashed and you want to update it without having to restart GOG
    # Galaxy or disconnect the plugin
    dist_path = os.path.join(DIST_DIR, f"{MANIFEST['platform']}_{MANIFEST['guid']}")
    copy_tree("src", dist_path)


@task
def install(c):
    dist_path = os.path.join(DIST_DIR, f"{MANIFEST['platform']}_{MANIFEST['guid']}")
    build(c, output=dist_path)


@task
def pack(c):
    output = f"{MANIFEST['platform']}_{MANIFEST['guid']}"
    release_path = os.path.join(
        RELEASE_DIR, f"{MANIFEST['platform']}_v{MANIFEST['version']}.zip"
    )
    if not os.path.isdir(RELEASE_DIR):
        os.mkdir(RELEASE_DIR)
    build(c, output=output, ziparchive=release_path)
    rmtree(output)
