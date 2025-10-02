## Django REST API — M4U (dev api branch)

### Links
- Local APIs: `http://127.0.0.1:8000/api/`
- Local Website (MVC): `http://127.0.0.1:8000/`
- Deployment: `https://phamquoctuan041203.pythonanywhere.com/`

### Description
JSON APIs for M4U music app: JWT authentication, songs, artists, genres, albums, favorites, and search.
Admin CRUD endpoints are provided for Song, Artist, Genre (require staff account).

---

## Setup

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

cd source
python manage.py migrate
python manage.py createsuperuser  # create staff if you need admin CRUD
python manage.py runserver
```

---

## Auth

JWT-based authentication:

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123","email":"u1@example.com"}'

# Login (get JWT tokens)
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123"}'

# Response: {"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...", "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}

# Authenticated profile
curl http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Refresh token (when access token expires)
curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<REFRESH_TOKEN>"}'

# Logout (blacklist refresh token)
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<REFRESH_TOKEN>"}'
```

---

## Endpoints

### Public
- `GET /api/songs/` — list songs (paginated optional)
- `GET /api/songs/{id}/` — song detail
- `GET /api/artists/` — list artists
- `GET /api/artists/{id}/` — artist detail
- `GET /api/genres/` — list genres
- `GET /api/genres/{id}/` — genre detail
- `GET /api/search/?query=...&genre=<id>` — search songs

### Authenticated (user)
- `GET /api/songs/favorites/` — list favorite songs
- `POST /api/songs/{id}/favorite/` — toggle favorite
- `GET /api/albums/` — list my albums
- `POST /api/albums/` — create album `{ name }`
- `GET|PUT|DELETE /api/albums/{id}/` — album detail/update/delete (owner only)
- `POST /api/albums/{album_id}/songs/{song_id}/add/` — add song to my album
- `DELETE /api/albums/{album_id}/songs/{song_id}/remove/` — remove song from my album

### Authentication Endpoints
- `POST /api/auth/register/` — register user
- `POST /api/auth/login/` — login (get JWT tokens)
- `POST /api/auth/refresh/` — refresh access token
- `POST /api/auth/logout/` — logout (blacklist refresh token)
- `GET /api/auth/profile/` — get user profile

### Admin (staff-only)
- `GET|POST /api/admin/songs/` — list/create song
- `GET|PUT|PATCH|DELETE /api/admin/songs/{id}/`
  - Song write fields: `title, cover_image, audio_file, lyrics, artist_id, genre_ids[]`
- `GET|POST /api/admin/artists/` — list/create artist
- `GET|PUT|PATCH|DELETE /api/admin/artists/{id}/`
- `GET|POST /api/admin/genres/` — list/create genre
- `GET|PUT|PATCH|DELETE /api/admin/genres/{id}/`

---

## Request examples

```bash
# Toggle favorite
curl -X POST http://127.0.0.1:8000/api/songs/1/favorite/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Create album
curl -X POST http://127.0.0.1:8000/api/albums/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" \
  -d '{"name":"My Favorites"}'

# Admin: create song (multipart for file fields)
curl -X POST http://127.0.0.1:8000/api/admin/songs/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -F "title=Hello" \
  -F "artist_id=1" \
  -F "genre_ids=1" -F "genre_ids=2" \
  -F "audio_file=@source/media/songs/Nuoc_Mat_Ca_Sau.mp3" \
  -F "cover_image=@source/media/covers/QT-1.jpg"
```