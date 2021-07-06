# Magic Minecraft Mod Modernizer
This is a WIP, wonderfully named script to automatically download latest versions of a Minecraft mod compatable with a given Minecraft version
## Running
To set up the config file, you can run the `setup.sh` file, or rename `mods.cfg.example` to `mods.cfg` and rename `settings.cfg.example` to `settings.cfg`. Put each mod on a new line in the format detailed in the header line. Comments with a `#` will be ignored.
**Example Configuration**
```ini
[MODRINTH]
sodium
lithium
phosphor
hydrogen
[GITHUB]
comp500/Indium
[CURSEFORGE]
# I'm just leaving this here in case Curseforge ever gets an API
```
## Strategies

### Modrinth
Currently has a mostly-working modrinth strategy, downloading compatible versions of listed mods from modrinth.

### Github Releases
There is a working™ Github Releases strategy. It relies on the minecraft version set inside the mod's gradle.properties to determine version, and as such doesn't understand "1.16.2-1.16.5" in the filename. This means that it will very rarely download an incompatable version, but may also not recognize all compatable versions. It also currently does not respect modloaders, and may download a fabric version when you wanted a forge version, or vice versa.

### Curseforge
Curseforge has no API to check mod versions with, so without parsing the webpages, there is no way to automatically detect and download new versions. 

## Todo
- [x] Add Github update strategy
- [x] Add a configuration option for Minecraft version
- [ ] Move/remove outdated mod versions in output folder
- [ ] Respect modloaders


## Credits
Mod name by [@NarwhalCat27](https://github.com/NarwhalCat27)
