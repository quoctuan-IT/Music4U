from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import RegisterForm, AlbumForm
from .models import Song, Album, Genre, Artist


def index(request):
    songs = Song.objects.all().order_by('-id')[:4]  # Hiển thị bài hát mới nhất trước
    genres = Genre.objects.all()
    artists = Artist.objects.all()

    return render(request, 'index.html', {'songs': songs, 'genres': genres, 'artists': artists})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)  # Tự động đăng nhập sau khi đăng ký

            return redirect('login')
        else:
            messages.error(request, "Register failed!")

    else:
        form = RegisterForm()

    return render(request, 'spotify/users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')  # Nếu đã login rồi thì chuyển về home

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Hi! {user.username}")

            return redirect('/')  # hoặc dashboard tùy bạn
        else:
            messages.error(request, "Login failed!")

    return render(request, 'spotify/users/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logout Success.")

    return redirect('login')


@login_required
def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    albums = Album.objects.filter(user=request.user)

    return render(request, 'spotify/songs/detail.html', {'song': song, 'albums': albums})


# Add a new song to favorites
@login_required
def song_favorite(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    user = request.user

    if song in user.favorite_songs.all():
        user.favorite_songs.remove(song)
        is_favorite = False
    else:
        user.favorite_songs.add(song)
        is_favorite = True

    # Return JSON if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})

    return redirect('/')


@login_required()
def user_profile(request):
    return render(request, 'spotify/users/profile.html')


@login_required()
def user_favorites(request):
    favorite_songs = request.user.favorite_songs.all()

    return render(request, 'spotify/songs/favorites.html', {'favorite_songs': favorite_songs})


@login_required()
def user_albums(request):
    albums = Album.objects.filter(user=request.user)

    return render(request, 'spotify/albums/albums.html', {'albums': albums})


@login_required
def album_detail(request, album_id):
    album = Album.objects.get(id=album_id, user=request.user)

    return render(request, 'spotify/albums/detail.html', {'album': album})


@login_required
def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)

        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            form.save_m2m()  # save songs to album - user
            messages.success(request, 'Album created successfully!')

            return redirect('albums')
    else:
        form = AlbumForm()

    return render(request, 'spotify/albums/create.html', {'form': form})


def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    album.delete()
    messages.success(request, "Album deleted successfully.")

    return redirect('albums')  # hoặc tên URL list album


@login_required
def song_album(request, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        album_id = request.POST.get('album_id')
        album = get_object_or_404(Album, id=album_id, user=request.user)

        if song in album.songs.all():
            messages.info(request, '🎵 This song is already in the album.')
        else:
            album.songs.add(song)
            messages.success(request, f'Song "{song.title}" was added to album "{album.name}".')

        return redirect('song_detail', song_id=song.id)


def remove_song_album(request, album_id, song_id):
    album = get_object_or_404(Album, id=album_id, user=request.user)
    song = get_object_or_404(Song, id=song_id)

    album.songs.remove(song)
    messages.success(request, f"Removed '{song.title}' from album.")

    return redirect('album_detail', album_id=album.id)


def search(request):
    query = request.GET.get('query', '')
    genre_id = request.GET.get('genre', '')
    artist_id = request.GET.get('artist', '')

    songs = Song.objects.all()

    if query:
        songs = songs.filter(title__icontains=query)

    if genre_id:
        songs = songs.filter(genre__id=genre_id)

    if artist_id:
        songs = songs.filter(artist__id=artist_id)

    genres = Genre.objects.all()
    artists = Artist.objects.all()

    context = {
        'songs': songs,
        'genres': genres,
        'artists': artists,
        'query': query,
        'selected_genre': genre_id,
        'selected_artist': artist_id,
    }

    return render(request, 'spotify/songs/search.html', context)
