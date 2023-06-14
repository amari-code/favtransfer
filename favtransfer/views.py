from django.shortcuts import render
from django.views.generic import View
from .secret_id import client_secret, client_id
from .forms import PlaylistForm
from .transfer import ArtistTransfer
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect

# class PlaylistsCreateView(FormView):
#     #model = Playlists
#     form_class = PlaylistForm
#     template_name = "playlist/playlist_form.html"
#     success_url = "/playlist/view"
#
#     def get(self, request, *args, **kwargs):
#         return render(request, "playlist/playlist_form.html")
#
#
#     def post(self, request, *args, **kwargs):
#         playid = PlaylistForm(request.POST)
#         play = playid.playlist_link
#         return render(request, "playlist/playlist_list.html", {'string_to_print': play})
#
# class PlaylistsListView(TemplateView):
#     # model = Playlists
#     # context_object_name = "playlists"
#     # template_name = "playlist/playlist_list.html"
#     template_name = "playlist/playlist_list.html"
#     context = {
#         "saluto" : "ciao"
#     }
#     def get(self, request):
#
#         return render(request, self.template_name,  self.context)
#
#     def post(self, request):
#         play = request.POST.get("playlist_link")
#         return render(request, self.template_name, {"play" : play})


class PlaylistView(View):

    at = 0


    def get(self, request):

        # print(f"args are: {access_token}")
        form = PlaylistForm()
        return render(request, "playlist/playlist_form.html", {"form": form})


    def post(self, request):
        form = PlaylistForm(request.POST)
        if form.is_valid():
            token_info = request.session.get('spotify_token')
            access_token = token_info['access_token']

            at = ArtistTransfer(access_token)

            print(at)

            link = form.cleaned_data['playlist_link']
            at.spotify_query(link)
            at.follower()
            artistlist = at.artist_list
            user_id = at.user_id
            return render(request, 'playlist/playlist_list.html', {'link_to_print': link, 'artists': artistlist, 'user' : user_id})
        else:
            return render(request, 'playlist/playlist_form.html', {'form': form})

def authorize_spotify(request):
    scope = 'playlist-read-private user-follow-modify'  # Add required scopes based on your application's needs
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8000/spotify-callback', scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8000/spotify-callback')
    code = request.GET.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code)
        # Store the token_info in the session or database for future API requests
        # You can also redirect the user to another page or perform additional actions here
        request.session['spotify_token'] = token_info
        print("success")
        return redirect('/playlist', tok=token_info)
    else:
        # Handle error or redirect to an error page
        return render(request, 'playlist/playlist_form.html', {'form': code})
