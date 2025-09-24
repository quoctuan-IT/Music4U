## M4U - Music Streaming Web 🎵

A full‑stack music streaming web app that lets users browse, play, and manage songs, favorite tracks, and personal albums. It supports authentication, artist and genre browsing, search with genre filters, and a responsive audio player.


## 🚀 Features

- **Admin**
  - Manage Songs, Users, Genres, Artists, Albums (Django Admin)

- **User**
  - Register / Login / Logout
  - Browse latest songs and view song details
  - Stream audio files served from the backend, auto‑play next track
  - Add/Remove songs from Favorites
  - Create personal Albums, add/remove songs in albums
  - Search songs by keyword and filter by Genre
  - Browse Artists and view Artist details with their songs


## 🛠️ Tech Stack

- Front‑end: HTML5, CSS3, Bootstrap 5
- Back‑end: Python 3, Django 5
- Database: MySQL


## 📦 Setup & Run
```bash

# 1) Clone
git clone https://github.com/quoctuan-IT/Music4U.git
cd Music4U

# 2) Create virtualenv (Windows)
python -m venv venv

# 3) Activate
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  # optional
venv\Scripts\activate

# 4) Install deps
pip install -r requirements.txt

# 5) Configure DB in source/project/settings.py (MySQL)

# 6) Migrate
cd source
python manage.py makemigrations
python manage.py migrate

# 7) Create superuser
python manage.py createsuperuser

# 8) Run server
python manage.py runserver

```


Static files are served in development when `DEBUG=True` with:
- `STATIC_URL = "/static/"`
- `STATICFILES_DIRS = [BASE_DIR / "static"]`

Media (cover images, audio files) are stored under `source/media/`.

Access:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`


## 🔗 Main Routes

- Home: `/`
- Register: `/register/`
- Login: `/login/`
- Logout: `/user/logout/`
- Profile: `/user/`
- Favorites: `/user/favorite/`

- Songs: `/songs/`
- Song detail: `/song/<song_id>/detail/`
- Toggle favorite (AJAX/POST): `/song/<song_id>/favorite/`
- Add song to album (POST): `/song/<song_id>/song-albums/`

- User albums: `/user/albums/`
- Album detail: `/user/album/<album_id>/detail/`
- Create album: `/user/album/create/`
- Delete album: `/user/album/<album_id>/delete/`
- Remove song from album: `/user/album/<album_id>/song/<song_id>/remove`

- Artists: `/artists/`
- Artist detail: `/artist/<artist_id>/detail/`

- Search: `/search/?query=...&genre=<genre_id>`


## 📚 Data Model

- `Artist(name, bio, image)`
- `Genre(name, description)`
- `Song(title, cover_image, audio_file, lyrics, artist(FK), genres(M2M), uploaded_by, created_at)`
- `Album(name, user, songs(M2M), created_at)`
- Each `User` has `favorite_songs` (ManyToMany to `Song`).


## 🎧 Player & Favorites

- Favorite button uses AJAX POST to `/song/<id>/favorite/`, returns JSON `{ is_favorite: true|false }` and updates the UI (Like/Liked).
- Audio player supports Play/Pause, Next, Previous, and artist song lists; auto‑advances to the next track on end.


## 🧪 Quick Test Flow

1) Create some `Artist`, `Genre`, `Song` via Admin.
2) Log in as a regular user, add songs to Favorites on the song card or detail page.
3) Create an `Album`, add songs; remove a song from album to verify the flow.
4) Use Search with keyword and Genre filter.
