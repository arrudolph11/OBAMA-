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
    pass

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
    pass

def main():
    #driver program here
    #make it interactive with user input a year
    #year = input('What year do you want to see how mainstream Obama's music is?')
    #if year == 2017: songs = get_obama_songs_2017

    print(get_spotify_playlist(2017))

if __name__ == "__main__":
    main()
