# Riot Integration - v0.2.3

Self explanatroy, a GOG Galaxy 2.0 Community integration for Riot! You can download it from [releases](https://github.com/urwrstkn8mare/galaxy-riot-integration/releases).

You can also install it using [scoop ](https://scoop.sh/) using this [bucket](https://github.com/borger/scoop-galaxy-integrations) by [borger](https://github.com/borger).

![games_example](https://raw.githubusercontent.com/urwrstkn8mare/gog-riot-integration/master/screenshot.png)

If you're wondering why the icon is odd (missing) see this [issue](https://github.com/urwrstkn8mare/gog-riot-integration/issues/1#issuecomment-641019594).

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

Any help (and feedback about this project) would be appreciated! If you want to add something or do a task feel free to do it and I'd appreciate a pull request.

- [ ] Add Mac support
- [x] ~~Automatically determine path to `RiotClientServices.exe`. (need to parse target path from Windows shortcuts. spoiler alert - it's hard)~~
- [ ] ~~Not require start menu shortcuts to be available.~~ (see this [issue](https://github.com/urwrstkn8mare/galaxy-riot-integration/issues/6))
- [ ] Support friend recomendation and presence. (this may not be possible though)

## Credits

- Heavy inspiration from <https://github.com/FriendsOfGalaxy/galaxy-integration-minecraft>, the fork of: <https://github.com/TouwaStar/Galaxy_Plugin_Minecraft>
- <https://github.com/tylerbrawl/Galaxy-Utils>
- And of course: <https://github.com/gogcom/galaxy-integrations-python-api>

## Development / Build Release

- Build Release: `python3 build.py -r`
- Test it in your own GOG Galaxy: `python3 build.py -d`
