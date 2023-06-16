#!/usr/bin/env python3


from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render
from django.views.generic import View
from decouple import config

from .forms import PlaylistForm
from .transfer import ArtistTransfer

import os
import spotipy


client_id = config("client_id")
client_secret = config("client_secret")
scope = 'playlist-read-private user-follow-modify'


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
            token_info = request.session.get(f'spotify_token')
            access_token = token_info['access_token']

            at = ArtistTransfer(access_token)

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

    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                            redirect_uri='http://localhost:8000/spotify-callback', scope=scope, show_dialog=True)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def spotify_callback(request):
    session = SessionStore()
    session.create()
    # Store the session key in a variable or pass it to another part of your code
    session_key = session.session_key
    sp_oauth = spotipy.oauth2.SpotifyOAuth(username=session_key, client_id=client_id, client_secret=client_secret,
                                           redirect_uri='http://localhost:8000/spotify-callback')

    code = request.GET.get('code')

    if code:
        token_info = sp_oauth.get_access_token(code)
        # Store the token_info in the session or database for future API requests
        # You can also redirect the user to another page or perform additional actions here
        request.session[f'spotify_token'] = token_info
        request.session['key'] = session_key
        request.GET.pop("code")
        return redirect("playlist.new")
    else:
        # Handle error or redirect to an error page
        return redirect("authorize_spotify")


def logout_spotify(request):
    os.remove(f".cache-{request.session.get('key')}")
    request.session.clear()
    cache.clear()
    return render(request, 'playlist/thanks.html')


def home(request):
    return render(request, 'playlist/home.html')
