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
    for album in os.listdir(os.path.join(config['directoryRoot'], artist)):
        print(f'\t{album}')
        artpath = fetcher.get_artwork_url(covergrabber.Album(f'{artist} - {album}'))
        response = requests.get(artpath)
        if response.status_code == 200:
            
            file_extension = pathlib.Path(artpath).suffix
            writepath = os.path.join(config["directoryOutput"],artist,album,f'folder{file_extension}')

            os.makedirs(os.path.join(config["directoryOutput"],artist), exist_ok=True)
            os.makedirs(os.path.join(config["directoryOutput"],artist,album), exist_ok=True)

            with open(writepath, 'wb') as f:
                f.write(response.content)

            for blacklistfile in os.listdir(config["directoryBlacklist"]):
                if filecmp.cmp(os.path.join(config["directoryBlacklist"], blacklistfile), writepath):
                    print(f'BLACKLIST: {blacklistfile}: {writepath}')
                    os.remove(writepath)
                    break