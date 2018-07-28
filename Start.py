import requests, bs4
import re
import numpy as np
from array import array
#hotnewhiphop = requests.get("https://www.hotnewhiphop.com/songs/")
#hotnewhiphop.raise_for_status()
#hhhsoup = bs4.BeautifulSoup(hotnewhiphop.text,"html.parser")


def html_cleaner(artist_products):
    artists = []
    for k in range(len(artist_products)):

        defaultRegex = re.compile(r"(<em class=\"default-artist\">|</em>)")
        artistMo = defaultRegex.findall(artist_products[k])

        artists.append((((artist_products[k])).replace(artistMo[1], "").replace(artistMo[0],"")))

    return (artists)


def find_artists_songs(url):
    hotnewhiphop = requests.get(url)
    hotnewhiphop.raise_for_status()
    hhhsoup = bs4.BeautifulSoup(hotnewhiphop.text, "html.parser")

    artist_products = []
    global songs
    songs = []

    artist_prods_html = (hhhsoup.findAll(class_="default-artist"))
    songtitle_prods_html = (hhhsoup.findAll(class_="cover-title"))

    for artist in artist_prods_html:
        artist_products.append(str(artist))
    for song in songtitle_prods_html:
        songs.append((song).get("title"))


    return artist_products

((html_cleaner(find_artists_songs("https://www.hotnewhiphop.com/songs/"))))

artists = html_cleaner(find_artists_songs("https://www.hotnewhiphop.com/songs/"))
artist_songs = np.array((artists, songs))
MyArtists = ["Kendrick Lamar", "Eminem", "Young Thug", "21 Savage", "Kanye West", "Fetty Wap", "A$AP Rocky",
             "Madeintyo", "Pusha T"]

def match_artists(MyArtists,artist_songs):
    matched_artists = []
    matched_songs = []

    for k in range(len(artists)):
        for artist in MyArtists:
            if artist_songs[0][k] == artist:
                matched_artists.append(artist_songs[0][k])
                matched_songs.append(artist_songs[1][k])
            else:
                continue
    matched_artists_songs = np.array((matched_artists,matched_songs),dtype=str)
    return matched_artists_songs

print (match_artists(MyArtists,artist_songs))

