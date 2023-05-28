import argparse
import os
import unicodedata
import shutil
import re
import json

CONFIG_READ_FAILURE = 1

class PlaylistExporter:
    
    def __init__(self):
        self.track_match = re.compile('^[0-9]+\S* ')
        self.config_path = 'config.json'
        self.config = {}
        self.prefix_length = 5
        
    def load_config(self):
        try:
            with open(self.config_path, 'r') as config_file:
                self.config = json.load(config_file)
                return True
        except Exception as ex:
            print(f"Error reading config file: {self.config_path} \n{ex}")
            return False

    def normalize_unicode(self, my_string):
        '''
        https://docs.python.org/3/howto/unicode.html
        '''
        return unicodedata.normalize('NFD', my_string)

    def find_track(self, trackname, folder):
        items = os.listdir(folder)
        found = False
        location = ''

        for item in items:
            itempath = os.path.join(folder, item)

            if os.path.isdir(itempath):
                found, location = self.find_track(trackname, itempath)
                if found:
                    break

            elif self.is_match(trackname, itempath):
                found = True
                location = itempath
                break

        return found, location

    def is_match(self, needle, haystack):
        exclude_chars = u'":_[]/\\?’’‘'

        try:
            path_to_track, track_file = os.path.split(haystack)
            needle = self.normalize_unicode(needle)
            track_file = self.normalize_unicode(track_file)

            for char in exclude_chars:
                track_file = track_file.replace(char, '')
                needle = needle.replace(char, '')

            needle = needle.replace("'", '').strip()
            track_file = track_file.replace("'", '').strip()  
            track_file_name, ext = os.path.splitext(track_file)
            search_name = self.remove_track_number(track_file_name)
            return needle == search_name and ext in self.config["supportedFileTypes"]
        
        except Exception as ex:
            print(f'Exception while matching track name: {ex}')
            return False

    def remove_track_number(self, track_name):
        if not self.track_match.match(track_name):
            return track_name
        first_space_index = track_name.find(' ')
        return track_name[first_space_index + 1:]

    def generate_prefix(self, index):
        str_index = str(index)
        prefix = ''
        padding_length = self.prefix_length - len(str_index)
        
        if padding_length < 0:
            return prefix

        for i in range(padding_length):
            prefix += '0'

        return prefix + str_index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('playlist')
    parser.add_argument('destination')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    exporter = PlaylistExporter()
    if not exporter.load_config():
        exit(CONFIG_READ_FAILURE)

    with open(args.playlist, 'r', encoding='utf-16') as list:
        content = list.read()

    lines = content.split('\n')
    tracks = []

    for line in lines[1:]:
        track = line.split('\t')[0].strip()
        if track is not None and len(track) > 0:
            tracks.append(track)

    found_tracks = 0
    missed_tracks = 0
    playlist_name, extension = os.path.splitext(args.playlist)
    destination_folder = os.path.join(args.destination, playlist_name)

    if args.test:
        print('Test mode: Skipping destination folder creation.')
    else:
        if os.path.exists(destination_folder):
            print('Folder already exists.')
        else:
            print(f'Creating folder {destination_folder}')
            os.mkdir(destination_folder)

    for track in tracks:
        result, track_path = exporter.find_track(track, exporter.config['iTunesPath'])

        if result:
            found_tracks += 1
            track_folder, track_filename = os.path.split(track_path)
            prefix = exporter.generate_prefix(found_tracks)
            adjusted_filename = f'{prefix}_{track_filename}'
            destination_path = os.path.join(destination_folder, adjusted_filename)
            print(f'Found track: {track} at path: {track_path}' + 
                  f'\nDestination file name: {adjusted_filename}')
            if not args.test:
                shutil.copy2(track_path, destination_path)
        else:
            missed_tracks += 1
            print(f'Did not find: {track}')

    print(f'Found {found_tracks} | missed {missed_tracks}')

    if args.test:
        print('Test mode: run complete, no tracks copied')


if __name__ == '__main__':
    main()
