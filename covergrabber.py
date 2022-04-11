#!/usr/bin/python3

import re
import requests
from lxml import html

class Album(object):
    """
    Album data and methods

    """
    def __init__(self, input_string, delim=" - "):

        # Splice our flat string into a dict for assigning self variables:
        input_dict = {}
        input_dict = self._splice_combined_string(input_string, delim)

        self.artist = input_dict["artist"]
        self.album = input_dict["album"]

    def _splice_combined_string(self, input_string, delim=" - "):
        """ 
        Split 'Album'delim'Artist' string, and return a dict
        
        :param input_string: <str> Input string, in 'Album - Artist' format
        :param delim: (Optional) <str> Optional delimiter to split by
        :return: <dict>
        """
        ret = {
            "artist": "",
            "album": ""
        }

        split_string = input_string.split(delim)
        ret["artist"] = split_string[0]
        ret["album"] = split_string[1]

        return ret

    def __str__(self):
        return str(self.__dict__)

class ArtworkFetcher(object):
    """ 
    Abstract Base Class for our fetcher implementations
    """

    def __init__(self):
        raise NotImplementedError

    def get_artwork_url(self, album):
        """
        Search for our album art, and return an url as string

        :param album: <Album> Our Album object to search service for
        :return: <str> URL where art is located
        """
        raise NotImplementedError

    def __str__(self):
        return str(self.__dict__)

class LastFMFetcher(ArtworkFetcher):
    """
    Concrete Class for Scraping Last.fm Services (naughty)
    """

    def __init__(self):

        self.base_url = "https://www.last.fm/music"
        self.meta_xpath_img = "/html/head/meta[@property='og:image']"

    def get_artwork_url(self, album):
        """
        Search for our album art, and return an url as string

        :param album: <Album> Our Album object to search service for
        :return: <str> URL where art is located
        """

        request_url = self.base_url + "/" + album.artist + "/" + album.album
        r = requests.get(request_url)

        tree = html.fromstring(r.content)
        raw_img_url = tree.xpath(self.meta_xpath_img)
        for r in raw_img_url:
            artwork_url = r.get("content")
            break
        
        # Check to see if the url is a file of some sort?
        match = re.search("\.[a-zA-Z]{3,4}$", artwork_url)
        if match:
            return artwork_url
        else:
            return ''

class FetcherEngine(object):
    """
    Fetcher Engine, for fetching album art.
    Strategy Design Pattern used to abstract API/Service used to fetch art
    through ArtworkFetcher Classes
    """

    def __init__(self):
        """
        Set default strategy (LastFM)
        """
        last_fm = LastFMFetcher()
        self.strategy = last_fm

    def set_lastfm(self):
        self.strategy = last_fm

    def get_artwork_url(self, album):
        url = self.strategy.get_artwork_url(album)
        return url