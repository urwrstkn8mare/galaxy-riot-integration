# Riot Integration - v0.1.1

Self explanatroy, a GOG Galaxy 2.0 Community integration for Riot! Note, this

## Usage

It's pretty simple. Just place unzip the file from [releases](https://github.com/urwrstkn8mare/gog-riot-integration/releases) and place the folder in `%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed`.

Note: As of now, the path to `RiotClientServices.exe` is set by default to `C:\Riot Games\Riot Client\RiotClientServices.exe`. To change it create a file called `riot_client_location.txt` and put the path to the executable in it. Then place the file in `%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed`.

## Known Issues

- ~~If you press sync integratiom games lose installed status for some reason (working on it right now!)~~

## Todo

Any help would be appreciated!

- [ ] Add Mac support
- [ ] Automatically determine path to `RiotClientServices.exe`.
- [ ] Maybe changed the formatting of the code to something other than [Black](https://github.com/psf/black). Its consistent but not as nice as some other styles of formatting.

## Credits

- Heavy inspiration from <https://github.com/FriendsOfGalaxy/galaxy-integration-minecraft>, the fork of: <https://github.com/TouwaStar/Galaxy_Plugin_Minecraft>
- <https://github.com/tylerbrawl/Galaxy-Utils>
- And of course: <https://github.com/gogcom/galaxy-integrations-python-api>
