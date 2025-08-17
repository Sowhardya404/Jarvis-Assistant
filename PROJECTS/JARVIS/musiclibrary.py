import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope=scope
))

def play_song(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[uri])
        return f"Playing {song_name}"
    else:
        return f"Song '{song_name}' not found on Spotify."

def pause_music():
    sp.pause_playback()
    return "Music paused."

def resume_music():
    sp.start_playback()
    return "Resumed music."

def stop_music():
    sp.pause_playback()
    sp.seek_track(0)
    return "Stopped music."
