from bs4 import BeautifulSoup
import requests
import re
import json
import unittest

#honestly might need a function for each year, since the source isn't in the same format
#his playlist for 2016 would be hard to scrape I think, so maybe we should do 2017-2020 at least for now

def get_obama_songs_2017():
    #https://www.rollingstone.com/music/music-news/barack-obama-names-kendrick-lamar-jay-z-u2-to-2017-favorite-songs-list-253740/
    #https://www.facebook.com/barackobama/posts/10155532677446749

    response = requests.get('https://www.facebook.com/barackobama/posts/10155532677446749')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraph = soup.find_all('div', class_ = 'o9v6fnle cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q')
        for i in paragraph:
            song = paragraph.find('div', dir = 'auto')
            obamas_songs.append(song.text)
    return obamas_songs

def get_obama_songs_2018():
    pass
def get_obama_songs_2019():
    pass
def get_obama_songs_2020():

#use requests, Spotify API gets spotify playlist for each year
def get_spotify_playlist(year):
    pass

#idk calculate popularity of each song, based on either the score from Spotify API or we could do the number rank it is on the Spotify playlist
def calc_song_pop(song):
    pass

def main():
    pass
