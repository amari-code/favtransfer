from django.urls import path

from . import views
from .views import authorize_spotify, spotify_callback

urlpatterns = [
    path('authorize-spotify/', authorize_spotify, name='authorize_spotify'),
    path('spotify-callback/', spotify_callback, name='spotify_callback'),
    path('playlist', views.PlaylistFView.as_view(), name="playlist.new"),
    # path('playlist/view', views.PlaylistView.as_view(), name="playlist.view"),
]