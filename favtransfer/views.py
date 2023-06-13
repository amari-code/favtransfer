from django.shortcuts import render
from django.views.generic import View

from .forms import PlaylistForm
from .transfer import ArtistTransfer

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

    at = ArtistTransfer()

    print(at)


    def get(self, request):
        form = PlaylistForm()
        return render(request, "playlist/playlist_form.html", {"form": form})


    def post(self, request):
        form = PlaylistForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['playlist_link']
            self.at.spotify_query(link)
            self.at.follower()
            artistlist = self.at.artist_list
            user_id = self.at.user_id
            return render(request, 'playlist/playlist_list.html', {'link_to_print': link, 'artists': artistlist, 'user' : user_id})
        else:
            return render(request, 'playlist/playlist_form.html', {'form': form})
