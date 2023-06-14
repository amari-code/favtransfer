from spotipy.oauth2 import SpotifyOAuth, SpotifyPKCE
from .secret_id import client_secret, client_id
import pandas as pd
import spotipy
from spotipy import util


class ArtistTransfer:

    def __init__(self, atk):
        self.artist_list = []
        self.SPOTIPY_CLIENT_ID = client_id
        self.SPOTIPY_CLIENT_SECRET = client_secret
        self.sp = self.spotify_auth(atk)
        self.user_id = self.sp.me()['id']

    def spotify_auth(self, atk):

        # Spotify authorization request
        # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
        #                                                client_secret=self.SPOTIPY_CLIENT_SECRET,
        #                                                redirect_uri='http://localhost:7777/callback',
        #                                                scope='playlist-read-private user-follow-modify'))
        # sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=self.SPOTIPY_CLIENT_ID,
        #                                               redirect_uri='http://localhost:7777/callback',
        #                                               scope='playlist-read-private user-follow-modify',
        #                                               ))
        sp = spotipy.Spotify(auth=atk)
        return sp

    def spotify_query(self, pl):
        tmp = []
        print(self.user_id)
        playlist = self.sp.playlist(pl)
        # pprint.pprint(playlist['tracks']['items'])
        for i in playlist['tracks']['items']:
            uri = i['track']['artists'][0]['external_urls']['spotify']
            artist_name = i['track']['artists'][0]['name']
            ID = i['track']['artists'][0]['id']
            tmp_s = [artist_name, uri, ID]
            tmp.append(tmp_s)
            # print(f'{artist_name} - {uri}')
        artist_list_tmp = pd.DataFrame(tmp, columns=['Name', 'URI', 'ID'])
        self.artist_list = artist_list_tmp.drop_duplicates()
        print(self.artist_list)

    def follower(self, unfollow=0):

        if unfollow:
            self.sp.user_unfollow_artists(self.artist_list['ID'])
        else:
            self.sp.user_follow_artists(self.artist_list['ID'])


# pl = 'https://open.spotify.com/playlist/5pVeWznNvTV1wimWkrVYeP?si=6366e2896084421f'
# AT = ArtistTransfer()
# AT.spotify_query(pl)
# AT.follower(1)

