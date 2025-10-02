## M4U - Music Streaming Web 🎵
## Deployment 🚀: https://phamquoctuan041203.pythonanywhere.com/

A full‑stack music streaming web app that lets users browse, play, and manage songs, favorite tracks, and personal albums. It supports authentication, artist and genre browsing, search with genre filters, and a responsive audio player.

**This project provides both:**
- **Django MVC**: Traditional web app with HTML templates
- **Django REST API**: JSON APIs for frontend integration


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

- **Front‑end**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Back‑end**: Python 3, Django 5, Django REST Framework
- **Database**: MySQL
- **Authentication**: Django Session (MVC) + JWT (API)


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
# Ensure INSTALLED_APPS includes: 'rest_framework', 'rest_framework_simplejwt'

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
- **MVC Web App**: `http://127.0.0.1:8000/`
- **REST API**: `http://127.0.0.1:8000/api/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`


## 🔗 Routes

### **MVC Web App Routes**
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

### **REST API Routes**

#### **Authentication**
- `POST /api/auth/register/` — Register user
- `POST /api/auth/login/` — Login (get JWT tokens)
- `POST /api/auth/refresh/` — Refresh access token
- `POST /api/auth/logout/` — Logout (blacklist refresh token)
- `GET /api/auth/profile/` — Get user profile

#### **Public Endpoints**
- `GET /api/songs/` — List songs
- `GET /api/songs/{id}/` — Song detail
- `GET /api/artists/` — List artists
- `GET /api/artists/{id}/` — Artist detail
- `GET /api/genres/` — List genres
- `GET /api/genres/{id}/` — Genre detail
- `GET /api/search/?query=...&genre=<id>` — Search songs

#### **Authenticated Endpoints**
- `GET /api/songs/favorites/` — List favorite songs
- `POST /api/songs/{id}/favorite/` — Toggle favorite
- `GET /api/albums/` — List my albums
- `POST /api/albums/` — Create album
- `GET|PUT|DELETE /api/albums/{id}/` — Album CRUD
- `POST /api/albums/{album_id}/songs/{song_id}/add/` — Add song to album
- `DELETE /api/albums/{album_id}/songs/{song_id}/remove/` — Remove song from album

#### **Admin Endpoints (Staff Only)**
- `GET|POST /api/admin/songs/` — Song CRUD
- `GET|POST /api/admin/artists/` — Artist CRUD
- `GET|POST /api/admin/genres/` — Genre CRUD


## 📚 Data Model

- `Artist(name, bio, image)`
- `Genre(name, description)`
- `Song(title, cover_image, audio_file, lyrics, artist(FK), genres(M2M), uploaded_by, created_at)`
- `Album(name, user, songs(M2M), created_at)`
- Each `User` has `favorite_songs` (ManyToMany to `Song`).


## 🎧 Player & Favorites

- **MVC**: Favorite button uses AJAX POST to `/song/<id>/favorite/`, returns JSON `{ is_favorite: true|false }` and updates the UI (Like/Liked).
- **API**: Use `POST /api/songs/{id}/favorite/` with JWT authentication.
- Audio player supports Play/Pause, Next, Previous, and artist song lists; auto‑advances to the next track on end.


## 🧪 Quick Test Flow

### **MVC Web App**
1) Create some `Artist`, `Genre`, `Song` via Admin.
2) Log in as a regular user, add songs to Favorites on the song card or detail page.
3) Create an `Album`, add songs; remove a song from album to verify the flow.
4) Use Search with keyword and Genre filter.

### **REST API**
```bash
# Register & Login
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123","email":"test@example.com"}'

curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Response: {"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...", "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}

# Use JWT access token for authenticated requests
curl http://127.0.0.1:8000/api/songs/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Refresh token when access token expires
curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<REFRESH_TOKEN>"}'

# Toggle favorite song
curl -X POST http://127.0.0.1:8000/api/songs/1/favorite/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Create album
curl -X POST http://127.0.0.1:8000/api/albums/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Favorites"}'
```
