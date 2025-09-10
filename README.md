## M4U - Music Streaming Web 🎵

A Full-Stack Web Application that allows Users to browse, play, and manage music playlists.
Includes features such as user authentication, song search, categorized genres, and a responsive audio player interface.


## 🚀 Features

- 👤 Admin:
  - ⚙️ Manage Songs, User Accounts, Genres, Artists, Albums
  
- 🧑 User:
  - 🔐 User authentication (JWT)
  - 🎵 Browse available songs
  - 🎧 Play music stored on the server
  - 🛒 Create and manage personal favorite songs and albums
  - 🔍 Search songs 


## 🛠️ Tech Stack

- **Front-End:** HTML + CSS + Bootstrap 5
- **Back-End:** Python 3 + Django
- **Database:** MySQL


## 📦 Setup & Installation

```bash

# Clone Repository
git clone https://github.com/quoctuan-IT/Music4U.git
cd Music4U

# Create Virtual Environment on Windows
python -m venv venv
venv\Scripts\activate
    
# Install Dependencies
pip install -r requirements.txt

# Configure Database => 'settings.py'
python manage.py makemigrations
python manage.py migrate

# Create Admin User
python manage.py createsuperuser

# Run the server
python manage.py runserver

# Deactivate Virtual Environment on Windows
deactivate