# GOG Galaxy Riot Integration

A GOG Galaxy 2.0 Community integration for Riot! You can download it from [releases](https://github.com/urwrstkn8mare/galaxy-riot-integration/releases). You can also install it using [scoop](https://scoop.sh/) using this [bucket](https://github.com/borger/scoop-galaxy-integrations) by [borger](https://github.com/borger).

![games_example](https://raw.githubusercontent.com/urwrstkn8mare/gog-riot-integration/master/screenshot.png)

[![version](https://img.shields.io/badge/version-v0.2.3-blue)](https://GitHub.com/urwrstkn8mare/galaxy-riot-integration/releases/)
[![latest downloads](https://img.shields.io/github/downloads/urwrstkn8mare/galaxy-riot-integration/v0.2.3/total.svg)](https://GitHub.com/urwrstkn8mare/galaxy-riot-integration/releases/)

_Note: If you're wondering why the icon is odd (missing) see this [issue](https://github.com/urwrstkn8mare/gog-riot-integration/issues/1#issuecomment-641019594)._

## Usage

It's pretty simple. Just unzip the file from [releases](https://github.com/urwrstkn8mare/gog-riot-integration/releases) and place the folder in `%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed`. Make sure to delete any other versions of this integration first and quit GOG Galaxy.

## [Known Issues](https://github.com/urwrstkn8mare/galaxy-riot-integration/labels/known%20issue)

See [known issues](https://github.com/urwrstkn8mare/galaxy-riot-integration/labels/known%20issue) in issues.

## Issues

When/if filing an issue please make sure to do the following:

1. Check [Known Issues](#known-issues).
2. Attach the log file for the integration. Can be found in `%programdata%\GOG.com\Galaxy\logs` and will have `riot` in its name.
3. Try earlier versions of the integration. It's really helpful to know if the issue was caused by a change I made in a newer version.

## FAQ

- _Game time doesn't show the time before I added the integration._
  That's because Riot doesn't record gametime. The integration will only display gametime while you've launched it via GOG Galaxy 2.0 just like if you had added it manually.

## Todo

Any help (and feedback about this project) would be appreciated! See [Contributing](#contributing).

- [ ] Add Mac support
- [x] ~~Automatically determine path to `RiotClientServices.exe`. (need to parse target path from Windows shortcuts. spoiler alert - it's hard)~~
- [ ] Solve [Games don't show up as installed if I didn't enable shortcuts before installing. #6](https://github.com/urwrstkn8mare/galaxy-riot-integration/issues/6). (see [issue](https://github.com/urwrstkn8mare/galaxy-riot-integration/issues/6) for progress - I've made some progress alr)
- [ ] [More precise game time #7](https://github.com/urwrstkn8mare/galaxy-riot-integration/issues/7)
- [ ] Support friend recomendation and presence. (this may not be possible though)

There may be more todos [here](https://github.com/urwrstkn8mare/galaxy-riot-integration/labels/todo).

## Contributing

Thanks in advance if you want to contribute! Feel free to complete and [todos](#todo) for me or add anything else you wanted to add. Then just submit a [pull request](https://github.com/urwrstkn8mare/galaxy-riot-integration/pulls)! If you don't understand something about the integration (eg. a part of the code - it may be hard to read sometimes) then feel free to ask me. You can do that via an issue, Discord ([GOG Café](https://discord.gg/bT2HJ9k)), or email (shaikhsamit@live.com). I also use some python scripts to build and test the integration so if you want, you can use it as well (see top of [build.py](build.py)).

## Credits

- Heavy inspiration from <https://github.com/FriendsOfGalaxy/galaxy-integration-minecraft>, the fork of: <https://github.com/TouwaStar/Galaxy_Plugin_Minecraft>
- <https://github.com/tylerbrawl/Galaxy-Utils>
- And of course: <https://github.com/gogcom/galaxy-integrations-python-api>
