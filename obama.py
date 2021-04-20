#SI 206 Final Project
#Team OBAMA: Claire Weadock and Amanda Rudolph

from bs4 import BeautifulSoup
import requests
import re
import json
import unittest

#honestly might need a function for each year, since the source isn't in the same format
#his playlist for 2016 would be hard to scrape I think, so maybe we should do 2017-2020 at least for now

def get_obama_songs_2017():
    response = requests.get('https://www.businessinsider.com/obama-favorite-songs-2017-2018-1#blessed-by-daniel-caesar-3')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraph = soup.find_all('div', class_ = 'slide')
        for i in paragraph:
            div = i.find('h2', class_ = 'slide-title-text')
            obamas_songs.append(div.text)
    return obamas_songs


def get_obama_songs_2018():
    response = requests.get('https://www.businessinsider.com/obama-favorite-songs-2018-12')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraph = soup.find_all('div', class_ = 'slide')
        for i in paragraph:
            div = i.find('h2', class_ = 'slide-title-text')
            obamas_songs.append(div.text)
    return obamas_songs
        
def get_obama_songs_2019():
    response = requests.get('https://www.cnn.com/2019/12/30/politics/barack-obama-favorite-music-2019-trnd/index.html')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        uls = soup.find('ul', class_ = 'list__items list__items--ul')
        lis = uls.find_all('li')
        for li in lis:
            obamas_songs.append(li.text)
    return obamas_songs

def get_obama_songs_2020():
    response = requests,get('https://www.nme.com/news/music/barack-obama-shares-his-top-songs-of-2020-with-new-spotify-playlist-2842698')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraph = soup.find_all('div', class_ = '#not sure what to put here....')
        for i in pragaraph:

#use requests, Spotify API gets spotify playlist for each year
#can't figure out how to use access token: BQA3-OIYlKUL8QUpXZPoOXBUzTygpRar5OoWeRWDHs3Rv0xrdVrgtyMwR6zNEB89ZyU_Qg0R2IZ2MYYpwjK8Q3JLlZy0_LVa4QWz1cjErGoy4V_VWLONlhKDKFTfmBlPTfqNQ5dSNKPFzqoxXA
def get_spotify_playlist(year):
    base_url = 'https://api.spotify.com/v1/playlists/{}/tracks'
    playlist_id = get_playlist_id(year)
    request_url = base_url.format(playlist_id)

    r = requests.get(request_url)
    data = r.text

    return data

def get_playlist_id(year):
    switcher = {2017: '37i9dQZF1DWTE7dVUebpUW', 2018: '37i9dQZF1DX1HUbZS4LEyL', 2019: '37i9dQZF1DXcz8eC5kMSWZ', 2020: '37i9dQZF1DX7Jl5KP2eZaS'}
    return switcher.get(year, "Invalid year")

#idk calculate popularity of each song, based on either the score from Spotify API or we could do the number rank it is on the Spotify playlist
def calc_song_pop(song):

def compare_obama_to_spotify(obamadict, spotifydict):
    #obamadict is a dictionary where the key is the year, and the values are 
    #obamas songs for that year

    #spotifydict is a dictionary where the key is the year, and the values are
    #spotifys top songs for that year

    #loop through each year for both dicts, find commonalities
    #im being dumb rn how do i do this
.
def main():
    #driver program here
    #make it interactive with user input a year
    #year = input('What year do you want to see how mainstream Obama's music is?')
    #if year == 2017: # songs = get_obama_songs_2017
    #if

    print(get_obama_songs_2019())

if __name__ == "__main__":
    main()
