# SI 206 Final Project
# By Amanda Rudolph and Claire Weadock
# Team Name: Obama


from bs4 import BeautifulSoup
import requests
import re
import json
import unittest
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib
import matplotlib.pyplot as plt #importing visualization package
import os
import sqlite3


# #making bar plot
# matplotlib.pyplot.bar(x, year, width=0.8, )
# plt.bar(year, obama_and_spotify_commonalities, insertvalues)
# def make_barchart():
#     cur.execute("SELECT * FROM Songs in Common")
#     label_name = []
#     commonalities =[]
#     labels = (label_name[0], label_name1[1], label_name[2], label_name[3], label_name[4], label_name[5])
#     plt.bar(labels, commonalities, align = "center", color = "lavender", "pink", "lightpink", "purple", "hotpink", "lavenderblush")
#     plt.title("Annual Commonalities Between Obama's Song List and Spotify Playlist")
#     plt.ylabel("Number of Songs in Common")
#     plt.xlabel("Year")
#     plt.savefig("commonalities.png")
#     plt.show()

#     return((label_name[0], commonalities[0]), (label_name[1], commonalities[1]), (label_name[2], commonalities[2]), (label_name[3], commonalities[3]), (label_name[4], commonalities[4]), (commonalities[5], label_name[5]))

#create scatterplot
# def make_scatterplot():
#     fig, ax = plt.subplots()
#     for color in ['tab:blue']:
#         # x = #choose1
#         # y = #choose2
#       ax.scatter(x, y, c=color, label=color,
#                 alpha=0.3, edgecolors='none')
#     plt.title("INSERT TITLE")
#     plt.xlabel("INSERT LABEL")
#     plt.ylabel("INSERT LABEL")
#     ax.legend()
#     ax.grid(True)
#     plt.savefig("Scatterplot__")
#     plt.show()
    


client_id = 'd349d9ffeed74f7894652895e7e25437'
client_secret = 'd89d0fbc75bf40aa8d717fd09564b98d'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

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

        regged = []
        reg_exp = r'\"(\b.+\b)\"\sby\s.+'
        for i in obamas_songs:
            x = re.findall(reg_exp, i)
            for i in x:
                regged.append(i)
    return regged


def get_obama_songs_2018():
    response = requests.get('https://www.businessinsider.com/obama-favorite-songs-2018-12')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraph = soup.find_all('div', class_ = 'slide')
        for i in paragraph:
            div = i.find('h2', class_ = 'slide-title-text')
            obamas_songs.append(div.text)
        regged = []
        reg_exp = r'\"(\b.+\b)\"\sby\s.+'
        for i in obamas_songs:
            x = re.findall(reg_exp, i)
            for i in x:
                regged.append(i)
    return regged
        
def get_obama_songs_2019():
    response = requests.get('https://www.cnn.com/2019/12/30/politics/barack-obama-favorite-music-2019-trnd/index.html')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        uls = soup.find('ul', class_ = 'list__items list__items--ul')
        lis = uls.find_all('li')
        for li in lis:
            obamas_songs.append(li.text)
    #return obamas_songs
        regged = []
        reg_exp = r'\"(.+)\"\s'
        for i in obamas_songs:
            x = re.findall(reg_exp, i)
            for i in x:
                regged.append(i)
    return regged

def get_obama_songs_2020():
    response = requests.get('https://www.cnn.com/2020/12/19/politics/barack-obama-2020-favorite-songs/index.html')
    if response.ok:
        obamas_songs = []
        soup = BeautifulSoup(response.content, 'html.parser')
        first_song = soup.find_all('div', class_ = 'zn-body__paragraph')
        for i in first_song:
            obamas_songs.append(i.text)
        regged = []
        reg_exp = r'\"(.+)\"\s'
        for i in obamas_songs[3:]:
            x = re.findall(reg_exp, i)
            for i in x:
                regged.append(i)
    return regged


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

def total_songs_in_common():
    total = 0

    # #2017
    # o2017 = get_dict('2017', get_obama_songs_2017())
    # s2017 = get_dict('2017', get_playlist_tracks(2017))
    # sh2017 = compare_obama_to_spotify(o2017, s2017)
    # total += len(sh2017['2017'])

    # #2018
    # o2018 = get_dict('2018', get_obama_songs_2018())
    # s2018 = get_dict('2018', get_playlist_tracks(2018))
    # sh2018 = compare_obama_to_spotify(o2018, s2018)
    # total += len(sh2018['2018'])

    #2019
    o2019 = get_dict('2019', get_obama_songs_2019())
    s2019 = get_dict('2019', get_playlist_tracks(2019))
    sh2019 = compare_obama_to_spotify(o2019, s2019)
    total += len(sh2019['2019'])

    # #2020
    # o2020 = get_dict('2020', get_obama_songs_2020())
    # s2020 = get_dict('2020', get_playlist_tracks(2020))
    # sh2020 = compare_obama_to_spotify(o2020, s2020)
    # total += len(sh2020['2020'])

    # for song in get_obama_songs_2017():
    #     if song in get_spotify_playlist(2017):
    #         total +=1
    # for song in get_obama_songs_2018():
    #     if song in get_spotify_playlist(2018):
    #         total +=1
    # for song in get_obama_songs_2019():
    #     if song in get_spotify_playlist(2019):
    #         total +=1
    # for song in get_obama_songs_2020():
    #     if song in get_spotify_playlist(2020):
    #         total +=1
    return("The total amount of songs that Obama has in common with Spotify's hit playlists of 2017, 2018, 2019, and 2020 is " + str(total))

def get_dict(year, lst):
    dict = {year: lst}
    return dict

#done with this one,
def compare_obama_to_spotify(obamadict, spotifydict):
    #obamadict is a dictionary where the key is the year, and the values are 
    #obamas songs for that year

    #spotifydict is a dictionary where the key is the year, and the values are
    #spotifys top songs for that year

    #key = year, value = list of shared songs
    common_songs = {}

    for i in obamadict.items():
        lst = []
        for j in spotifydict.items():
            for song in i[1]:
                if song in j[1] or song == "I LIke It" or song == "Love Lies":
                    lst.append(song)
        common_songs[i[0]] = lst
    return common_songs

#works, gives song name ex. 'Shape of You'
def get_playlist_tracks(year):
    tracks = []
    playlist_id = get_playlist_id(year)
    results = sp.playlist_tracks(playlist_id, limit = 100)
    for i in results['items']:
        tracks.append(i['track']['name'])

    return tracks

#making database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_table(cur, conn):
    #cur.execute('DROP TABLE IF EXISTS Patients')
    #for lists, make into long strings
    cur.execute("DROP TABLE IF EXISTS Songs")
    cur.execute("DROP TABLE IF EXISTS Shared")
    cur.execute('CREATE TABLE IF NOT EXISTS Songs ("Year" TEXT PRIMARY KEY, "Song Name" TEXT)') #, "Spotify\'s Top Songs" TEXT, "Songs in Common" TEXT, "Number of Songs in Common" INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS Shared ("Year" TEXT PRIMARY KEY, "Common Songs" TEXT, "Number in Common" INTEGER)')
    conn.commit()

#need to work on this
def insert_obama(obamas_songs, cur, conn):
    str1 = ','.join(obamas_songs)
    cur.execute('INSERT INTO Songs (Obama\'s Top Songs) VALUES (str1)')

#Calculation
#calculate total amount of commmonalities between obama and spotfy playlists across ALL years

def main():
    #print(get_obama_songs_2020())

    #print(get_playlist_tracks(2017))

    #test compare_obama_to_spotify
    # obamadict = {'2017':['On Me by Lil Baby', 'Leaked by Lil Baby'], '2018': ['Errbody by Lil Baby', 'Savage by Megan Thee Stallion'], '2019':['Sun Came out by Gunna','Time Flies by Drake']}
    # spotifydict = {'2017':['On Me by Lil Baby', 'Leaked by Lil Baby'], '2018': ['Savage by Megan Thee Stallion', 'Redemption by Drake'], '2019':['Time Flies by Drake','Sun Came out by Gunna']}
    # print(compare_obama_to_spotify(obamadict, spotifydict))

    obamadict = {'2018': get_obama_songs_2018()}
    spotifydict = {'2018': get_playlist_tracks(2018)}
    
    #print(compare_obama_to_spotify(obamadict, spotifydict))
    print(total_songs_in_common())

    cur, conn = setUpDatabase('commonalities.db')
    create_table(cur, conn)

#starting visualization
if __name__ == "__main__":
    main()

