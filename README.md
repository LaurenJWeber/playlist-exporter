# playlist-exporter

Find all the tracks from an iTunes playlist and copy them to an external drive, e.g. USB stick.

## Why is this needed?

This was developed because the UConnect entertainment unit in our new car did not interoperate well with our older iPod (7th Gen Classic).
It often would not recognize the iPod was connected, and would frequently need the iPod to be rebooted.  The entertainment unit has no trouble, however, reading audio files from a USB drive.

## Caveats

Most music purchased from iTunes will be downloaded as `.mp3` or `.m4a` files.  UConnect recognizes these.  However, you will also get the occasional `.m4p` file which UConnect does not recognize.  For each track that is stored this way: Go into iTunes > > Create AAC version, which will make a `.m4a` copy of the file.

## Usage instructions

1. Ensure python >= 3.10 is installed on the computer holding your iTunes library.
2. Clone this repository: `git clone https://github.com/LaurenJWeber/playlist-exporter.git`
3. Edit the `config.json` file.  Set the path to your iTunes library.  Save the file.
4. Plug in a freshly-formatted USB drive and note its path, for example `/Volumes/MyUSBDrive`.
5. In iTunes, go to File > Export playlist and save it as a text file, e.g. `/Users/me/MyPlaylist.txt`
6. Invoke the script and pass it the paths to the Playlist text file and USB drive as arguments:
    `python export_playlist.py /Users/me/MyPlaylist.txt /Volumes/MyUSBDrive`
7. The script will:
   * Create a folder with your playlist name e.g. `MyPlaylist` on the USB drive
   * Search in the iTunes library for each track in your playlist
   * When found, copy it to the folder on the USB drive, prefixing it with an index number to preserve the track order, e.g. 00001_MySong1, 00002_MySong2, etc.
8. When finished, the script will print how many tracks were copied, and if any were missed, e.g. could not be found.
