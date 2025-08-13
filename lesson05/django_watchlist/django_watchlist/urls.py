from django.contrib import admin
from django.urls import path
# Static version: from django.views.generic import TemplateView
from watchlist.views import home_view, watchlist_view

urlpatterns = [
    # Static version: path("", TemplateView.as_view(template_name="watchlist/home.html"), name="home"),
    path("", home_view, name="home"),
    path("watchlist/", watchlist_view, name="watchlist"), # added later
    path("admin/", admin.site.urls),
]