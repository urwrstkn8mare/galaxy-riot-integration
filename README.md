# Riot Integration - v0.1.3

Self explanatroy, a GOG Galaxy 2.0 Community integration for Riot! If you're wondering why the icon is odd (missing) see this [issue](https://github.com/urwrstkn8mare/gog-riot-integration/issues/1#issuecomment-641019594). For more information, see [Usage](#usage).

![games_example](https://raw.githubusercontent.com/urwrstkn8mare/gog-riot-integration/master/screenshot.png)

## Usage

It's pretty simple. Just unzip the file from [releases](https://github.com/urwrstkn8mare/gog-riot-integration/releases) and place the folder in `%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed`.

## Known Issues

- _Games don't show up as installed_ They may not show up as installed **if you didn't enable shortcuts** when installing them. While the plugin now uses the registry meaning you don't have to specify the the location of `RiotClientServices.exe`, Riot Games for some reason doesn't add a registry entry unless you enable shortcuts. If you didn't enable shortcuts you would have also noticed you can't find the games in Programs & Features, that is why. Unfortunately this is up to Riot Games to fix. Fortunately, however, you can delete both the desktop shorcuts and start menu shortcuts after.

## FAQ

- _Game time doesn't show the time before I added the plugin._
  That's because Riot doesn't record gametime. The plugin will only display gametime while you've launched it via GOG Galaxy 2.0 just like if you had added it manually.

## Todo

Any help (and feedback about this project) would be appreciated! If you want to add something or do a task feel free to do it and I'd appreciate a pull request.

- [ ] Add Mac support
- [x] ~~Automatically determine path to `RiotClientServices.exe`. (need to parse target path from Windows shortcuts. spoiler alert - it's hard)~~
- [ ] ~~Not require start menu shortcuts to be available.~~ (see [Known Issues](#known-issues))
- [ ] Support friend recomendation and presence. (this may not be possible though)

## Credits

- Heavy inspiration from <https://github.com/FriendsOfGalaxy/galaxy-integration-minecraft>, the fork of: <https://github.com/TouwaStar/Galaxy_Plugin_Minecraft>
- <https://github.com/tylerbrawl/Galaxy-Utils>
- And of course: <https://github.com/gogcom/galaxy-integrations-python-api>

## Development / Build Release

- Build Release: `python3 build.py -r`
- Test it in your own GOG Galaxy: `python3 build.py -d`
