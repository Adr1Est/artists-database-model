from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    fav_artists = db.relationship("FavArtists", backref="user", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Artist(db.Model):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    listeners: Mapped[int] = mapped_column(unique=False, nullable=True)
    image: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)
    genre: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)

    albums = db.relationship("Album", backref="artist", cascade="all, delete")
    fav_by = db.relationship("FavArtists", backref="artist", cascade="all, delete")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "listeners": self.listeners,
            "image": self.image,
            "genre": self.genre
        }

class Album(db.Model):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    image: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"))

    songs = db.relationship("Song", backref="album", cascade="all, delete")

    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "image": self.image
        }

class Song(db.Model):
    __tablename__ = "song"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    album_id: Mapped[int] = mapped_column(ForeignKey("album.id"))
    duration: Mapped[int] = mapped_column(unique=False, nullable=False)
    preview: Mapped[str] = mapped_column(String(255), unique=False, nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "album_id": self.album_id,
            "duration": self.duration,
            "preview": self.preview
        }
    
class FavArtists(db.Model):
    __tablename__ = "fav_artists"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"), primary_key=True)

    def serialize(self):
        return{
            "user_id": self.user_id,
            "artist_id": self.artist_id
        }