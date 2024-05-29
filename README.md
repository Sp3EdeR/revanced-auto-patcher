# ReVanced Automatic Patcher
This script patches Android applications to change their behaviour. Patches are provided by the [ReVanced](https://github.com/revanced/revanced-patches) or [ReVanced Extended](https://github.com/inotia00/revanced-patches) projects.

## Prerequisites
The script requires [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) 3 or above to be installed on the computer. Python can be downloaded from [this link](https://www.python.org/downloads), or your operating system's official package manager. The ReVanced tools require Java SDK 11 or above to be installed on the computer. It is recommended to get it from [this link](https://www.azul.com/downloads/?package=jdk#zulu) or your operating system's official package manager.

## Patching
Both [ReVanced](https://github.com/ReVanced) and [ReVanced Extended](https://github.com/inotia00/) support a limited list of applications and versions. Trying to patch an unsupported application or a supported app's unsupported version will result in errors. The list of supported applications and their versions can be found at the following links:

* [ReVanced](https://revanced.app/patches) (This site has a short update delay)
* [ReVanced Extended](https://github.com/inotia00/revanced-patches#readme)

The original version of the application must be downloaded before patching can begin. To download a compatible version of the APK file, it is recommended to get it from [APKMirror](https://www.apkmirror.com/), since that site is a fairly safe download source. Find direct links to popular applications below (but choose compatible versions):

* [Facebook](https://www.apkmirror.com/apk/facebook-2/facebook/)
* [Facebook Messenger](https://www.apkmirror.com/apk/facebook-2/messenger/)
* [Instagram](https://www.apkmirror.com/apk/instagram/instagram-instagram/)
* [Lightroom Photo & Video Editor](https://www.apkmirror.com/apk/adobe/lightroom/) (by Adobe)
* [Recorder](https://www.apkmirror.com/apk/google-inc/google-recorder/) (by Google)
* [Reddit](https://www.apkmirror.com/apk/redditinc/reddit/)
* [Spotify](https://apkpure.com/spotify-music-and-podcasts-for-android/com.spotify.music) (warning, not on APKMirror!)
* [Spotify Lite](https://apkpure.com/spotify-lite/com.spotify.lite) (warning, not on APKMirror!)
* [Strava](https://www.apkmirror.com/apk/strava-inc/strava-running-and-cycling-gps/)
* [TikTok](https://www.apkmirror.com/apk/tiktok-pte-ltd/tik-tok/)
* [Trakt](https://www.apkmirror.com/apk/trakt/trakt/)
* [Tumblr](https://www.apkmirror.com/apk/tumblr-inc/tumblr/)
* [Twitch](https://www.apkmirror.com/apk/twitch-interactive-inc/twitch/)
* [X / Twitter](https://www.apkmirror.com/apk/x-corp/twitter/)
* [YouTube](https://www.apkmirror.com/apk/google-inc/youtube/)
* [YouTube Music](https://www.apkmirror.com/apk/google-inc/youtube-music/)

# Default Usage - Automatic Source Downloading
This method automatically downloads everything needed (from [APKMirror](https://www.apkmirror.com) and [Github](https://github.com)), and creates the patched APK file. By default, the script uses [ReVanced patches](https://github.com/ReVanced/revanced-patches) to modify APKs. Only place supported APKs, and only supported versions in this folder, otherwise the patching will fail. Create the following folder structure:

```
ReVanced
└── patch.py
```

Then run `python patch.py --help` and look at the output in the terminal. Select one or more applications from the list of supported ones, and run `python patch.py <app name>` or `python patch.py <app name> <app2 name> ...`. The patched apk will be created in the ReVanced directory. The following section documents the other files created.

# Default Usage - Manual Source Downloading
This is an alternative method that requires you to get the APK file for the original, unpatched application. By default, the script uses [ReVanced patches](https://github.com/ReVanced/revanced-patches) to modify APKs. Only place supported APKs, and only supported versions in this folder, otherwise the patching will fail. Create the following folder structure:

```
ReVanced
├── patch.py
├── SomeAppToPatch 10.5.2.apk
└── OtherAppToPatch 1.0.0.apk
```

Then run `python patch.py`. After the script finishes running, you will get the following folder structure:

```
ReVanced
├── tools
│   ├── revanced-cli-*.*.*-all.jar
│   ├── revanced-integrations-*.*.*.apk
│   └── revanced-patches-*.*.*.jar
├── patch.keystore
├── patch.py
├── SomeAppToPatch.json
├── SomeAppToPatch 10.5.2.apk
├── OtherAppToPatch.json
├── OtherAppToPatch 1.0.0.apk
├── RV SomeAppToPatch 10.5.2.apk
└── RV OtherAppToPatch 1.0.0.apk
```

Where the created directories / files are:

* `tools`: Contains the downloaded ReVanced patches used to patch your APK. Keeping these files can save internet bandwidth when re-patching your APKs.
* `patch.keystore`: Your unique keys with which the generated APKs were signed. Keep this file to be able to upgrade existing, installed software with newer versions without needing to uninstall the older version.
* `*.json` files: These files store patch options for the application. Initially these contain default options, but you can edit these files to build customised versions of the patched application.
* `RVX *.apk`: These are the generated, patched APKs, ready for you to install them.

# Edited Usage

It is possible to relatively easily edit the default behaviour of the patcher script. To edit its default behaviour, open the file in any other text editor application (on Windows you can use notepad). Look for the following text near the top of the file:

```json
# The following are the default settings. Edit to change the defaults.
settings = {
```

The text lines following this contain the configuration of how the script behaves when run without command-line arguments. Each configurable line has a comment (followed by the # character), which explains what that option controls. Change any of these values (to valid ones) to customise the script's behaviour.

For example, to create a directory that applies ReVanced patches, set up a directory as explained in the [Default Usage section](#default-usage), then edit the following line of patch.py from:

```py
'defaultPatchSource': 'rv',
```

to:

```py
'defaultPatchSource': 'rvx',
```

This makes the script use ReVanced Extended patches instead of ReVanced in that folder. The usage remains the same otherwise.

# Command-line Options

It is possible to thoroughly customise the script's behaviour using command-line arguments, without editing the script. To see the available arguments, run `python patch.py --help`. This will explain the usage of the the command-line interface.
