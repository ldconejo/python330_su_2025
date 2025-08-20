from django.db import models


class Platform(models.Model):
    platform = models.CharField(max_length=100)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.platform

class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre


class Show(models.Model):
    title = models.CharField(max_length=255)
    season = models.SmallIntegerField()
    image_url = models.URLField(blank=True)
    watched = models.BooleanField(default=False)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return f"{self.title} Season {self.season}"