from django.shortcuts import render
from .models import Platform, Show

def home_view(request):
    platforms = Platform.objects.all()
    return render(request, template_name="watchlist/home.html", context={"platforms": platforms})

def watchlist_view(request):
    all_shows = Show.objects.all()
    return render(request, template_name="watchlist/watchlist.html", context={"all_shows": all_shows})
