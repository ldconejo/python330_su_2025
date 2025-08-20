from rest_framework import serializers

from .models import Show, Platform, Genre

from rest_framework.exceptions import NotFound

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True, read_only=True)
    genre_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    platform = serializers.StringRelatedField(read_only=True)
    platform_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Show
        fields = [
            'id',
            'title',
            'season',
            'image_url',
            'watched',
            'platform',
            'platform_id',
            'genres',
            'genre_ids',
        ]

    def create(self, validated_data):
        platform_id = validated_data.pop('platform_id')
        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            raise NotFound(f'Platform {platform_id} not found')
        genre_ids = []
        if validated_data.get('genre_ids'):
            genre_ids = validated_data.pop('genre_ids')
        show = Show.objects.create(platform=platform, **validated_data)
        for genre_id in genre_ids:
            try:
                genre = Genre.objects.get(id=genre_id)
            except Genre.DoesNotExist:
                raise NotFound(f'Genre {genre_id} not found')
            show.genres.add(genre)
        show.save()
        return show
    
    def update(self, instance, validated_data):
        platform_id = validated_data.pop('platform_id')
        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            raise NotFound(f'Platform {platform_id} not found')
        instance.title = validated_data.get('title', instance.title)
        instance.season = validated_data.get('season', instance.season)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.watched = validated_data.get('watched', instance.watched)
        instance.platform = platform
        genre_ids = []
        if validated_data.get('genre_ids'):
            genre_ids = validated_data.pop('genre_ids')
            instance.genres.clear()
        for genre_id in genre_ids:
            try:
                genre = Genre.objects.get(id=genre_id)
            except Genre.DoesNotExist:
                raise NotFound(f'Genre {genre_id} not found')
            instance.genres.add(genre)
        instance.save()
        return instance
