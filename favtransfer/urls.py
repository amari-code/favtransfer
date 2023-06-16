from django.urls import path

from . import views


urlpatterns = [
    path('authorize-spotify/', views.authorize_spotify, name='authorize_spotify'),
    path('spotify-callback/', views.spotify_callback, name='spotify_callback'),
    path('playlist', views.PlaylistFView.as_view(), name="playlist.new"),
    path('playlist-view', views.PlaylistView.as_view(), name="playlist.view"),
    path('logout-spotify/', views.logout_spotify, name='logout.spotify'),
    path('', views.home, name='home')
]