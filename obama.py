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

""" 
Creating a Bar Plot where the x-axis is the Year and the y-axis is the amount (count) of songs Obama has in Commmon with Spotify's playlist the year
"""

def make_barchart(cur):
    commonalities = []
    years = []
    cur.execute("SELECT Year, NumberInCommon FROM Shared")
    for row in cur:
        if row[0] not in years:
            years.append(row[0])
            commonalities.append(row[1])
    label_name = ['2017', '2018', '2019', '2020']
    labels = (label_name[0], label_name[1], label_name[2], label_name[3])
    plt.bar(labels, commonalities, align = "center", color = ["lavender", "pink", "lightpink", "purple", "hotpink"])
    plt.title("Annual Commonalities Between Obama's Song List and Spotify Playlist")
    plt.ylabel("Number of Songs in Common")
    plt.xlabel("Year")
    plt.savefig("commonalities.png")
    plt.show()

    return((label_name[0], commonalities[0]), (label_name[1], commonalities[1]), (label_name[2], commonalities[2]), (label_name[3], commonalities[3]), (label_name[4], commonalities[4]))

""" 
Creating a Scatter Plot where the x-axis is the year and the y-axis is the percentage of Obama's songs are in Spotify's playlist that year.

"""
def make_scatterplot(cur):
    percentages = []
    numcommon = []
    years = [] #'2017', '2018', '2019', '2020']
    cur.execute('SELECT Year, NumberInCommon, LengthOfSpotifyPlaylist FROM Shared')
    for row in cur:
        if row[0] not in years:
            years.append(row[0])
            numcommon.append(row[1])
            percentages.append(row[1]/row[2])
            
    plt.scatter(years, percentages)
    plt.title("Percentage of Songs Obama has in Common with Spotify's Top Hits Playlist")
    plt.xlabel("Year")
    plt.ylabel("Percentage of Songs Shared")
    # ax.legend()
    # ax.grid(True)
    plt.savefig("ScatterplotPercentages")
    plt.show()
    
def make_char_scatterplot(cur):
    songs_chars = []
    song_years = []
    #songs_nums = [1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    commons_chars = []
    common_years = []
    cur.execute('SELECT Songs.Name, Songs.SongYear, Shared.CommonSongs, Shared.Year FROM Songs JOIN Shared ON Songs.SongYear = Shared.Year')
    for row in cur:
        songs_chars.append(len(row[0]))
        song_years.append(int(row[1]))
        commons_chars.append(len(row[2]))
        common_years.append(int(row[3]))
    
    plt.scatter(song_years, songs_chars, c = 'blue')
    plt.scatter(common_years, commons_chars, c = 'pink')
    plt.show()

client_id = 'd349d9ffeed74f7894652895e7e25437'
client_secret = 'd89d0fbc75bf40aa8d717fd09564b98d'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""
Getting Obama's favorite songs from 2017
"""
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

"""
Getting Obama's favorite songs from 2018
"""
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
"""
Getting Obama's favorite songs from 2019.
"""
def get_obama_songs_2019():
    tracks = []
    results = sp.playlist_tracks('37i9dQZF1DX9uhxIrnqGy3', limit = 100)
    for i in results['items']:
        tracks.append(i['track']['name'])
    return tracks
"""
Getting Obama's favorite songs from 2020
"""
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

def get_playlist_id(year):
    switcher = {2017: '37i9dQZF1DWTE7dVUebpUW', 2018: '37i9dQZF1DX1HUbZS4LEyL', 2019: '37i9dQZF1DWVRSukIED0e9', 2020: '37i9dQZF1DX7Jl5KP2eZaS'}
    return switcher.get(year, "Invalid year")

def total_songs_in_common():
    total = 0

    #2017
    o2017 = get_dict('2017', get_obama_songs_2017())
    s2017 = get_dict('2017', get_playlist_tracks(2017))
    sh2017 = compare_obama_to_spotify(o2017, s2017)
    total += len(sh2017['2017'])

    #2018
    o2018 = get_dict('2018', get_obama_songs_2018())
    s2018 = get_dict('2018', get_playlist_tracks(2018))
    sh2018 = compare_obama_to_spotify(o2018, s2018)
    total += len(sh2018['2018'])

    #2019
    o2019 = get_dict('2019', get_obama_songs_2019())
    s2019 = get_dict('2019', get_playlist_tracks(2019))
    sh2019 = compare_obama_to_spotify(o2019, s2019)
    total += len(sh2019['2019'])

    # #2020
    o2020 = get_dict('2020', get_obama_songs_2020())
    s2020 = get_dict('2020', get_playlist_tracks(2020))
    sh2020 = compare_obama_to_spotify(o2020, s2020)
    total += len(sh2020['2020'])
    return("The total amount of songs that Obama has in common with Spotify's hit playlists of 2017, 2018, 2019, and 2020 is " + str(total))

def get_dict(year, lst):
    dict = {year: lst}
    return dict


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
    results = sp.playlist_tracks(playlist_id)
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
    cur.execute('CREATE TABLE IF NOT EXISTS Songs ("SongYear" TEXT, "Name" TEXT)') #, "Spotify\'s Top Songs" TEXT, "Songs in Common" TEXT, "Number of Songs in Common" INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS Shared ("Year" TEXT, "CommonSongs" TEXT, "NumberInCommon" INTEGER, LengthOfSpotifyPlaylist INTEGER)')
    conn.commit()

#need to work on this
def insert_obama_first_25(obama_dict, cur, conn):
    index = 0
    #items = obama_dict.values()
    for key in obama_dict:
        for x in obama_dict[key]:
            if index < 25:
                cur.execute('INSERT INTO Songs (SongYear, Name) VALUES (?,?)', (key, x))
                index += 1
            else:
                insert_obama_rest(index, obama_dict, cur, conn)
                break
    conn.commit()

def insert_obama_rest(num, obama_dict, cur, conn):
    index = num
    for key in obama_dict:
        for i in obama_dict[key][25:]:
            cur.execute('INSERT INTO Songs (SongYear, Name) VALUES (?,?)', (key, i))
    conn.commit()

def insert_shared(obama_dict, year, cur, conn):
    sdict = {year: get_playlist_tracks(year)}
    shared_songs_dict = compare_obama_to_spotify(obama_dict, sdict)
    splaylists_lengths = [len(get_playlist_tracks(2017)), len(get_playlist_tracks(2018)), len(get_playlist_tracks(2019)), len(get_playlist_tracks(2020))]
    for key in shared_songs_dict:
        for i in shared_songs_dict[key]:
            index = 0
            cur.execute('INSERT INTO Shared (Year, CommonSongs, NumberInCommon, LengthOfSpotifyPlaylist) VALUES (?,?,?,?)', (key, i, len(shared_songs_dict[key]), splaylists_lengths[index]))
            index += 1
    if year == 2020:
        cur.execute('INSERT INTO Shared (Year, CommonSongs, NumberInCommon, LengthOfSpotifyPlaylist) VALUES (?,?,?,?)', (2020, 'No Common Songs', 0, 100))

    conn.commit()

def main():
    #test compare_obama_to_spotify
    # obamadict = {'2017':['On Me by Lil Baby', 'Leaked by Lil Baby'], '2018': ['Errbody by Lil Baby', 'Savage by Megan Thee Stallion'], '2019':['Sun Came out by Gunna','Time Flies by Drake']}
    # spotifydict = {'2017':['On Me by Lil Baby', 'Leaked by Lil Baby'], '2018': ['Savage by Megan Thee Stallion', 'Redemption by Drake'], '2019':['Time Flies by Drake','Sun Came out by Gunna']}
    # print(compare_obama_to_spotify(obamadict, spotifydict))

    o2017 = {'2017': get_obama_songs_2017()}
    o2018 = {'2018': get_obama_songs_2018()}
    o2019 = {'2019': get_obama_songs_2019()}
    o2020 = {'2020': get_obama_songs_2020()}
    spotifydict = {'2019': get_playlist_tracks(2019)}

    # print(obamadict)
    # print("SPOTIFY -----------------")
    # print(spotifydict)    
    #print(compare_obama_to_spotify(obamadict, spotifydict))
    #print(total_songs_in_common())

    cur, conn = setUpDatabase('commonalities.db')
    create_table(cur, conn)
    insert_obama_first_25(o2017, cur, conn)
    insert_obama_first_25(o2018, cur, conn)
    insert_obama_first_25(o2019, cur, conn)
    insert_obama_first_25(o2020, cur, conn)

    insert_shared(o2017, 2017, cur, conn)
    insert_shared(o2018, 2018, cur, conn)
    insert_shared(o2019, 2019, cur, conn)
    insert_shared(o2020, 2020, cur, conn)

    # make_barchart(cur)
    #make_scatterplot(cur)
    make_char_scatterplot(cur)



#starting visualization
if __name__ == "__main__":
    main()

