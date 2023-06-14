
from .secret_id import client_secret, client_id
import pandas as pd
import spotipy


class ArtistTransfer:

    def __init__(self, atk):
        self.artist_list = []
        self.SPOTIPY_CLIENT_ID = client_id
        self.SPOTIPY_CLIENT_SECRET = client_secret
        self.sp = self.spotify_auth(atk)
        self.user_id = self.sp.me()['id']

    def spotify_auth(self, atk):

        sp = spotipy.Spotify(auth=atk)
        return sp

    def spotify_query(self, pl):
        tmp = []
        print(self.user_id)
        playlist = self.sp.playlist(pl)
        for i in playlist['tracks']['items']:
            uri = i['track']['artists'][0]['external_urls']['spotify']
            artist_name = i['track']['artists'][0]['name']
            ID = i['track']['artists'][0]['id']
            tmp_s = [artist_name, uri, ID]
            tmp.append(tmp_s)
        artist_list_tmp = pd.DataFrame(tmp, columns=['Name', 'URI', 'ID'])
        self.artist_list = artist_list_tmp.drop_duplicates()
        print(self.artist_list)

    def follower(self, unfollow=0):

        if unfollow:
            self.sp.user_unfollow_artists(self.artist_list['ID'])
        else:
            self.sp.user_follow_artists(self.artist_list['ID'])
