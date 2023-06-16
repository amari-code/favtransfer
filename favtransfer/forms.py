from django import forms


# form where to paste the playlist
class PlaylistForm(forms.Form):
    playlist_link = forms.CharField(max_length=100)
