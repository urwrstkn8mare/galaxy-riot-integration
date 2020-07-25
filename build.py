# Source: https://gist.github.com/urwrstkn8mare/78d8377562d8719f3bd1f72f9c4e7516
# Just a python script I made to make testing plugins in GOG Galaxy easier as
# well as building the final zip to release. The integration and its files must
# be in a 'src' folder. Note: this works but the code is really bad pls don't judge.
# If you want to improve it feel free to fork it or just leave a comment with suggestions.

# Usage: python build.py -h

import sys, shutil, subprocess, os, glob, getopt, json

dirname = os.path.dirname(os.path.realpath(__file__))
src = os.path.join(dirname, "src")
platform = json.load(open(os.path.join(src, "manifest.json"), "r"))["platform"]


def ask(txt, auto_yes=False):
    if auto_yes:
        return True
    q = input(f"{txt} [Y/n] ").strip()
    if q == "Y":
        return True
    elif q == "n":
        return False
    else:
        print("Incorrect input. Assuming 'n'.")
        return False


def did_error(p, abort=None):
    err = p.communicate()[1]
    if err is not None and "exception" in err.decode():
        print("--Error--\n", err)
        print("There was an error. Aborting...")
        if abort is not None:
            abort()
        return True
    return False


def build(*, out=None, plat=None):
    # Adapted from:
    # https://github.com/FriendsOfGalaxy/galaxy-integrations-updater/blob/24e5157d3f5b473dc9efa0bcfb23b90f4be6be01/scripts.py#L373
    def abort():
        shutil.rmtree(out)

    print("Building...")
    if plat is None:
        if sys.platform == "win32":
            pip_platform = "win32"
        elif sys.platform == "darwin":
            pip_platform = "macosx_10_13_x86_64"
    else:
        pip_platform = plat
    print(f"pip-platform: {pip_platform}")
    out = os.path.join(dirname, "out") if out is None else os.path.abspath(out)
    print(f"out directory: {out}")
    if os.path.isdir(out):
        print("Removing exisiting out directory.")
        shutil.rmtree(out)
    print("Copying src directory to out directory.")
    shutil.copytree(src, out, shutil.ignore_patterns("*.pyc"))
    print("Creating compiled-requirements.txt")
    compiled_requirements = os.path.join(out, "compiled-requirements.txt")
    f = open(compiled_requirements, mode="w")
    p = subprocess.Popen(
        f'pip-compile "{os.path.join(dirname,"requirements.txt")}" --output-file=-',
        stdout=f,
        shell=True,
        stderr=subprocess.PIPE,
    )
    p.wait()
    f.close()
    if did_error(p, abort):
        return
    print("Installing packages")
    cmd = [
        f'"{sys.executable}" -m pip install',
        f'-r "{compiled_requirements}"',
        f"--platform {pip_platform}",
        f'-t "{out}"',
        "--python-version 37",
        "--no-compile",
        "--no-deps",
        "--default-timeout=60",
    ]
    p = subprocess.Popen(" ".join(cmd), shell=True, stdout=sys.stdout)
    p.wait()
    if did_error(p, abort):
        return


def release(plat=None):
    # not recommended to build for a platform on a platform which is not that
    # platform.
    if plat is None:
        plat = sys.platform
    if plat not in ["win32", "darwin"]:
        print("Unknown platform/os. Cannot continue.")
        return
    if plat == "win32":
        plat_name = "windows"
    elif plat == "darwin":
        plat_name = "mac"
    print(f"Making release for: {plat_name}")
    name = f"galaxy-{platform}-integration-{plat_name}"
    temp_out = os.path.join(dirname, "temp-out")
    os.mkdir(temp_out)
    out = os.path.join(dirname, temp_out, name)
    build(out=out, plat=plat)
    print("Cleaning up...")
    for dir_ in glob.glob(f"{out}/*.dist-info"):
        shutil.rmtree(dir_)
    for dir_ in glob.glob(f"{out}/*__pycache__"):
        shutil.rmtree(dir_)
    for test in glob.glob(f"{out}/**/test_*.py", recursive=True):
        os.remove(test)
    os.remove(os.path.join(out, "compiled-requirements.txt"))
    if zip:
        zip_path = os.path.join(dirname, f"{name}.zip")
        print(f"Zipping to: {zip_path}")
        if os.path.isfile(zip_path):
            os.remove(zip_path)
        shutil.make_archive(zip_path.replace(".zip", ""), "zip", temp_out)
        shutil.rmtree(temp_out)


def main():
    if sys.version_info.major != 3:
        print("Python 3 must be used to run this program.")
        return
    opts = getopt.getopt(sys.argv[1:], "drhy", ["out=", "plat="])
    if len(opts[0]) == 0:
        build()
    else:
        opts_dict = dict(opts[0])
        auto_yes = False
        if "-y" in opts_dict.keys():
            auto_yes = True
        if shutil.which("pip-compile") is None:
            if ask("'pip-tools' is not installed but is required. Install? ", auto_yes):
                p = subprocess.Popen(
                    f'"{sys.executable}" -m pip install pip-tools', shell=True, stdout=sys.stdout
                )
                p.wait()
                if did_error(p):
                    return
            else:
                return
        if "-h" in opts_dict.keys():
            print(
                """
Help (args):
    -h      Get some help.
    -d      Build for dev/testing in GOG Galaxy. Does not clean up but
            automatically puts it in the GOG Galaxy installed folder.
    -r      Build release files (zips).
    -y      Say yes to any prompts.
    --out   Specify the output folder/directory.
    --plat  Specify the platform to be built for. Best to just use the
            platform being built on.
You can only use one short option in a command. The program will use the
one first in the order displayed above. Long options and -y will be used
wherever applicable. Look at the code in build.py and the information at
the top for more info.
                """
            )
            return
        elif "-d" in opts_dict.keys():
            print("building in GOG Galaxy's installed directory for dev/testing")
            if sys.platform == "win32":
                installed_dir = "%localappdata%\\GOG.com\\Galaxy\\plugins\\installed"
            elif sys.platform == "darwin":
                installed_dir = "~/Library/Application Support/GOG.com/Galaxy/plugins/installed"
            else:
                print("unkown os/platform")
                return
            installed_dir = os.path.abspath(os.path.expandvars(os.path.expanduser(installed_dir)))
            for i in os.listdir(installed_dir):
                manifest = os.path.join(installed_dir, i, "manifest.json")
                if os.path.isfile(manifest):
                    if json.load(open(manifest, "r"))["platform"] == platform:
                        if ask(
                            f"Found existing plugin for this platform ({i}), remove? Warning GOG Galaxy must be closed before this.",  # noqa: E501
                            auto_yes,
                        ):
                            exisitng_plugin_path = os.path.join(installed_dir, i)
                            shutil.rmtree(exisitng_plugin_path)
                            print(f"Removed existing plugin: {exisitng_plugin_path}")
                        else:
                            print("Failed")
                            return
            out = os.path.join(installed_dir, f"{platform}_test_plugin")
            build(out=out)
        else:
            out, plat = None, None
            if "--out" in opts_dict.keys():
                out = opts_dict["--out"].strip()
            if "--plat" in opts_dict.keys():
                plat = opts_dict["--plat"].strip()
            if "-r" in opts_dict.keys():
                release(plat=plat)
            else:
                build(out=out, plat=plat)
    print("Done")


if __name__ == "__main__":
    main()
