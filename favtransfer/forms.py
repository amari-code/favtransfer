from django import forms


class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=10)
    playlist_link = forms.CharField(max_length=100)
