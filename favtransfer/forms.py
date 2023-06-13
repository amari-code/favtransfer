from django import forms
from django.core.exceptions import ValidationError

from .models import Playlists


# class PlaylistForm(forms.Form):
#     class Meta:
#         #model = Playlists
#         fields = ["text",]
#         widgets = {
#             "text": forms.Textarea(attrs={"class": "form-control mb-5"})
#         }
#         labels = {
#             "text": "Paste your playlist here:"
#         }
class PlaylistForm(forms.Form):
    playlist_link = forms.CharField(max_length=100)
