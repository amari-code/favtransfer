from django.contrib import admin

from .models import Playlists

class PlaylistsAdmin(admin.ModelAdmin):
    list_display = ['text',]

admin.site.register(Playlists, PlaylistsAdmin)
