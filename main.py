#!/usr/bin/python3

import os
import re
import json
import filecmp
import requests
import pathlib
from lxml import html

import covergrabber

# Load config:
with open('config.json', 'r') as j:
    config = json.load(j)

fetcher = covergrabber.FetcherEngine()

for artist in os.listdir(config['directoryRoot']):
    print(artist)
    for album in os.listdir(f'{config["directoryRoot"]}/{artist}'):
        print(f'\t{album}')
        albumObject = covergrabber.Album(f'{artist} - {album}')
        artpath = fetcher.get_artwork_url(albumObject)
        response = requests.get(artpath)
        if response.status_code == 200:
            
            file_extension = pathlib.Path(artpath).suffix
            with open(f'{config["directoryOutput"]}/{artist} - {album}{file_extension}', 'wb') as f:
                f.write(response.content)

            for blacklistfile in os.listdir(config["directoryBlacklist"]):
                print(f'{config["directoryBlacklist"]}/{blacklistfile}')
                if filecmp.cmp(f'{config["directoryBlacklist"]}/{blacklistfile}', f'{config["directoryOutput"]}/{artist} - {album}{file_extension}'):
                    print(f'BLACKLIST: {blacklistfile}: {artist} - {album}{file_extension}')
                    os.remove(f'{config["directoryOutput"]}/{artist} - {album}{file_extension}')
                    break