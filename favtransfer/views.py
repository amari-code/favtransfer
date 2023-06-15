import os
from decouple import config
from django.shortcuts import render
from django.views.generic import View
from .forms import PlaylistForm
from .transfer import ArtistTransfer
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib.sessions.backends.db import SessionStore

client_id = config("client_id")
client_secret = config("client_secret")


class PlaylistFView(View):

    @staticmethod
    def get(request):

        form = PlaylistForm()
        return render(request, "playlist/playlist_form.html", {"form": form})


class PlaylistView(View):

    @staticmethod
    def post(request):
        form = PlaylistForm(request.POST)
        if form.is_valid():
            print(f"session key:{request.session.get('key')}")
            token_info = request.session.get(f'spotify_token')
            access_token = token_info['access_token']

            at = ArtistTransfer(access_token)

            print(at)

            link = form.cleaned_data['playlist_link']
            at.spotify_query(link)
            at.follower()
            artistlist = at.artist_list
            user_id = at.user_id
            return render(request, 'playlist/playlist_list.html', {'link_to_print': link, 'artists': artistlist,
                                                                   'user': user_id})
        else:
            return render(request, 'playlist/playlist_form.html', {'form': form})


def authorize_spotify(request):
    scope = 'playlist-read-private user-follow-modify'  # Add required scopes based on your application's needs
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                            redirect_uri='http://localhost:8000/spotify-callback', scope=scope,
                            cache_handler=spotipy.CacheHandler())
    print(f"sp_oauth: {sp_oauth}")
    auth_url = sp_oauth.get_authorize_url()
    print(f"auth url:{auth_url}")
    return redirect(auth_url)


def spotify_callback(request):
    print(f"request: {request}")
    session = SessionStore()
    session.create()
    # Store the session key in a variable or pass it to another part of your code
    session_key = session.session_key
    print(f"session_key: {session_key}")
    sp_oauth = spotipy.oauth2.SpotifyOAuth(username=session_key, client_id=client_id, client_secret=client_secret,
                                           redirect_uri='http://localhost:8000/spotify-callback')
    code = request.GET.get('code')

    if code:
        token_info = sp_oauth.get_access_token(code)
        # Store the token_info in the session or database for future API requests
        # You can also redirect the user to another page or perform additional actions here
        request.session[f'spotify_token'] = token_info
        request.session['key'] = session_key
        return redirect('/playlist')
    else:
        # Handle error or redirect to an error page
        return render(request, 'playlist/playlist_form.html', {'form': code, 'session_key': session_key})


def logout_spotify(request):
    # Clear the session data
    os.remove(f".cache-{request.session.get('key')}")
    request.session.clear()
    cache.clear()

    return render(request, 'playlist/thanks.html')


def home(request):
    return render(request, 'playlist/home.html')
