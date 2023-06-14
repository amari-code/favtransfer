from django.urls import path

from . import views
from .views import authorize_spotify, spotify_callback, logout_spotify, home

urlpatterns = [
    path('authorize-spotify/', authorize_spotify, name='authorize_spotify'),
    path('spotify-callback/', spotify_callback, name='spotify_callback'),
    path('playlist', views.PlaylistFView.as_view(), name="playlist.new"),
    path('playlist-view', views.PlaylistView.as_view(), name="playlist.view"),
    path('logout-spotify/', logout_spotify, name='logout_spotify'),
    path('thanks/', logout_spotify, name='logout_spotify'),
    path('', home, name='home')
]