from django.shortcuts import render
from .models import Platform, Show, Genre

from rest_framework import viewsets
from .serializers import ShowSerializer, PlatformSerializer, GenreSerializer

def home_view(request):
    platforms = Platform.objects.all()
    return render(request, template_name="watchlist/home.html", context={"platforms": platforms})

def watchlist_view(request):
    all_shows = Show.objects.all()
    return render(request, template_name="watchlist/watchlist.html", context={"all_shows": all_shows})

class ShowViewSet(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
