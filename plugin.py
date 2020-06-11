from windows import WindowsRiotPlugin
from mac import MacRiotPlugin
import platform, sys
from galaxy.api.plugin import create_and_run_plugin


def main():
    plat = platform.system().lower()
    classes = {"windows": WindowsRiotPlugin, "darwin": MacRiotPlugin}
    create_and_run_plugin(classes.get(plat, None), sys.argv)


if __name__ == "__main__":
    main()
