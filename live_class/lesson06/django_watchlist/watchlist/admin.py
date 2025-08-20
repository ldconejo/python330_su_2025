from django.contrib import admin

from .models import Genre, Platform, Show

admin.site.register(Show)
admin.site.register(Genre)
admin.site.register(Platform)
