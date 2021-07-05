# Mod Updater (pending better name)
This is a WIP script to automatically download latest versions of a Minecraft mod compatable with a given Minecraft version
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
Currently has a mostly-working modrinth strategy, downloading mods from modrinth

### Github Releases
Planned, but not added yet™

### Curseforge
Curseforge has no API to check mod versions with, so without parsing the webpages, there is no way to automatically detect and download new versions. 

## Todo
- [ ] Add Github update strategy
- [x] Add a configuration option for Minecraft version