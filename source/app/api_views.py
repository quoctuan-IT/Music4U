from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import Song, Artist, Genre, Album

from .serializers import (
    SongSerializer,
    ArtistSerializer,
    GenreSerializer,
    AlbumSerializer,
    UserSerializer,
)


class IndexAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "index api"})


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id})

        return Response({"error": "Invalid credentials"}, status=400)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id})


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."})


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# Songs
class SongListAPIView(generics.ListAPIView):
    queryset = Song.objects.all().order_by("-created_at")
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]


class SongDetailAPIView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.AllowAny]


class FavoriteSongListAPIView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorite_songs.all()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    user = request.user

    if song in user.favorite_songs.all():
        user.favorite_songs.remove(song)
        is_favorite = False
    else:
        user.favorite_songs.add(song)
        is_favorite = True

    return Response({"is_favorite": is_favorite})


# Artists
class ArtistListAPIView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]


class ArtistDetailAPIView(generics.RetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]


# GENRES
class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]


class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]


# Albums
class AlbumListAPIView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def album_add_song(request, album_id, song_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    song = get_object_or_404(Song, id=song_id)

    if song in album.songs.all():
        return Response({"message": "Song already in album"}, status=400)

    album.songs.add(song)
    return Response({"message": f"Song '{song.title}' added to album '{album.name}'"})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def album_remove_song(request, album_id, song_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    song = get_object_or_404(Song, id=song_id)

    if song not in album.songs.all():
        return Response({"message": "Song not in album"}, status=400)

    album.songs.remove(song)
    return Response(
        {"message": f"Song '{song.title}' removed from album '{album.name}'"}
    )


# Search
@api_view(["GET"])
def search_songs(request):
    query = request.GET.get("query", "")
    genre_id = request.GET.get("genre", "")

    songs = Song.objects.all()

    if query:
        songs = songs.filter(title__icontains=query)

    if genre_id:
        songs = songs.filter(genres__id=genre_id)

    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)
