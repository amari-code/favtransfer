from django.urls import path

from . import views

urlpatterns = [
    path('playlist', views.PlaylistView.as_view(), name="playlist.new"),
    # path('playlist/view', views.PlaylistView.as_view(), name="playlist.view"),
]