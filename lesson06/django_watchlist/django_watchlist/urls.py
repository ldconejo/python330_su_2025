from django.contrib import admin
from django.urls import path, include # Import include for the browsable API component
# Static version: from django.views.generic import TemplateView

# from watchlist.views import home_view, watchlist_view --> Replaced by a new import
# New imports
from rest_framework import routers
from watchlist import views

# Router definition
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'shows', views.ShowViewSet, basename='shows')

# Routers for platforms and genres
router.register(r'platforms', views.PlatformViewSet, basename='platforms')
router.register(r'genres', views.GenreViewSet, basename='genres')

urlpatterns = [
    path("", views.home_view, name="home"), # Updated to add .views
    path("watchlist/", views.watchlist_view, name="watchlist"), # Updated to add .views
    path("api/", include(router.urls)), # New path using routers
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')), # Add this to support browsable API
    path("admin/", admin.site.urls),
]