> [!IMPORTANT]
> This repository is now archived. As of archiving, [@BellezaEmporium](https://github.com/BellezaEmporium) has done good work in his fork ([BellezaEmporium/galaxy-riot-integration](https://github.com/BellezaEmporium/galaxy-riot-integration)) and you should find a maintained version of this integration there. 

# GOG Galaxy Riot Integration

A GOG Galaxy 2.0 Community integration for Riot!

[![0.2.6](https://img.shields.io/badge/version-0.2.6-blue)](https://github.com/BellezaEmporium/galaxy-riot-integration/releases/tag/0.2.6)
[![MIT License](https://img.shields.io/github/license/BellezaEmporium/galaxy-riot-integration)](https://github.com/BellezaEmporium/galaxy-riot-integration/blob/master/LICENSE)
[![v0.2.6 Downloads](https://img.shields.io/github/downloads/BellezaEmporium/galaxy-riot-integration/0.2.6/total.svg)](https://github.com/BellezaEmporium/galaxy-riot-integration/releases/tag/0.2.6)

![games_example](https://raw.githubusercontent.com/BellezaEmporium/galaxy-riot-integration/master/screenshot.png)

## Usage / Installation

1. Download the latest release from [releases](https://github.com/BellezaEmporium/galaxy-riot-integration/releases).
2. Make sure to delete any other versions of this integration first and quit GOG Galaxy ['Settings' -> 'Exit'].
3. Unzip the file from [releases](https://github.com/BellezaEmporium/gog-riot-integration/releases) and place the folder in `%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed`.
4. Go to GOG Galaxy, open settings, and then go to the integrations tab. You should see `Riot` in the list of integrations and just click `connect`.

### Alternatives

- Alternatively you can install it easily using [scoop](https://scoop.sh/) using this [bucket](https://github.com/borger/scoop-galaxy-integrations) by [borger](https://github.com/borger).
- You can also use [Slashbunny](https://github.com/Slashbunny)'s [GOG Galaxy Plugins Downloader](https://github.com/Slashbunny/gog-galaxy-plugin-downloader).

## [Known Issues](https://github.com/BellezaEmporium/galaxy-riot-integration/issues?q=label%3A%22known+issue%22+)

See [known issues](https://github.com/BellezaEmporium/galaxy-riot-integration/issues?q=label%3A%22known+issue%22+) in [issues](https://github.com/BellezaEmporium/galaxy-riot-integration/issues). They will have the [known issue](https://github.com/BellezaEmporium/galaxy-riot-integration/issues?q=label%3A%22known+issue%22+) [label](https://github.com/BellezaEmporium/galaxy-riot-integration/labels).

## Issues

When/if filing an issue please make sure to do the following:

1. Check [Known Issues](#known-issues).
2. Attach the log file for the integration. Can be found in `%programdata%\GOG.com\Galaxy\logs` and will have `riot` in its name.
3. Try earlier versions of the integration. It's really helpful to know if the issue was caused by a change I made in a newer version.

## FAQ

- _Game time doesn't show the time before I added the integration._
  That's because Riot doesn't record gametime. The integration will only display gametime while you've launched it via GOG Galaxy 2.0 just like if you had added it manually.

## Todo

- Get previous game time tracking to work (Needs validation from the Tracker.gg team into production, as the API key is invalid for now)

## Contributing

Thanks in advance if you want to contribute! Feel free to complete any [todos](#todo) for me or add anything else you want to add. Then just submit a [pull request](https://github.com/BellezaEmporium/galaxy-riot-integration/pulls)! If you don't understand something about the integration (eg. a part of the code - it may be hard to read sometimes) then please feel free to ask me. You can do that via an [issue](https://github.com/BellezaEmporium/galaxy-riot-integration/issues/new), Discord ([GOG Café](https://discord.gg/bT2HJ9k)). I also use some python scripts to build and test the integration so if you want, you can use it as well (see [top of tasks.py](tasks.py#L1-L10) for more information about how to use it and more).

## Credits

- urwrstkn8mare for the base version of this integration : <https://github.com/urwrstkn8mare>
- Heavy inspiration from: <https://github.com/TouwaStar/Galaxy_Plugin_Minecraft>
- <https://github.com/tylerbrawl/Galaxy-Utils>
- And of course: <https://github.com/gogcom/galaxy-integrations-python-api>
