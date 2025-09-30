from rest_framework import serializers
from .models import Song, Artist, Genre, Album
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name", "description"]


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "name", "bio", "image"]


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = [
            "id",
            "title",
            "cover_image",
            "audio_file",
            "lyrics",
            "artist",
            "genres",
            "uploaded_by",
            "created_at",
        ]


class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ["id", "name", "songs", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    favorite_songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "favorite_songs"]
