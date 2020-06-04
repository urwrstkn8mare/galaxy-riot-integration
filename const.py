from galaxyutils.config_parser import get_config_options, Option

CONFIG_OPTIONS = get_config_options(
    [Option(option_name="win-install-location")]
)

WIN_INSTALL_LOCATION = CONFIG_OPTIONS["win-install-location"]
