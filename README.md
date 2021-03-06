# Thumper Modding Tool
A text-based editor for adding custom levels to Thumper.

## Installation
Download the [latest release](https://github.com/RainbowUnicorn7297/thumper-modding-tool/releases) and unzip to any folder.

## Getting Started
* Run "Thumper Modding Tool.exe" and select where the Thumper folder is located for first time setup.
* Click Turn ON Mod Mode button to backup your save data and replace all original levels with custom levels.
* Click Turn OFF Mod Mode button to restore the original levels and your save data.
* To edit the custom levels, open and edit the .txt files under the levels folder. Click Update Custom Levels button to commit any edits you have made.

## Editing Custom Levels
* Each custom level must contain the level config file (config_*\<level name\>*.txt) and .xfm Object file (xfm_*\<level name\>*.txt).
* The templates folder contains objects from the original levels. They can be copied and used in the custom levels, as long as the object names (obj_name) are not duplicated.
* The examples folder contains examples showcasing how various objects can be defined and used in a custom level.

## Troubleshooting
### Cloud Sync Conflict
In some occasions, Steam might detect there is a conflict between the cloud files and local files after turning ON/OFF Mod Mode:

![Cloud Sync Conflict](https://steamcdn-a.akamaihd.net/steam/support/faq/cloud_conflict.JPG)

You should always choose "Upload to the Steam Cloud". If "Download to this machine" is selected, you may end up with a save file without any scores. In this case, you can manually restore the save data from the backup folder of this modding tool to the savedata folder under the Thumper folder.
