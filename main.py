#!/usr/bin/python3

import os
import re
import json
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