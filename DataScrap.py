import spotipy
import spotipy.util as util
import pandas as pd

CLIENT_ID = "e5ff7ce4bf2340b4a9f072e10fc31767"
CLIENT_SECRET = "449e0a6d29ca41048d7673a9f0e4def0"
REDIRECT_URI = "http://localhost:8888/callback"
USERNAME = "mhfmtzz9e96snjn9ajhifx51k"
PLAYLIST_ID = "4g4S2NG2UVgQ40FgLXdWpz"

# Get a Spotify OAuth token
token = util.prompt_for_user_token(USERNAME, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
sp = spotipy.Spotify(auth=token)

# Get the playlist information
playlist = sp.user_playlist(USERNAME, PLAYLIST_ID)

# Get the tracks in the playlist using pagination
tracks = []
results = sp.playlist_tracks(PLAYLIST_ID)
tracks.extend(results['items'])
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Iterate through each track and extract relevant information
track_info = []
for track in tracks:
    # Get the track metadata
    track_data = track["track"]
    track_id = track_data["id"]
    track_name = track_data["name"]
    track_artist = track_data["artists"][0]["name"]
    track_popularity = track_data["popularity"]
    track_duration = track_data["duration_ms"]
    track_album = track_data["album"]["name"]
    track_release_date = track_data["album"]["release_date"]

    # Get the audio features for the track
    track_features = sp.audio_features(track_id)[0]
    try:
        track_danceability = track_features["danceability"]
        track_energy = track_features["energy"]
        track_loudness = track_features["loudness"]
        track_speechiness = track_features["speechiness"]
        track_acousticness = track_features["acousticness"]
        track_instrumentalness = track_features["instrumentalness"]
        track_liveness = track_features["liveness"]
        track_valence = track_features["valence"]
        track_tempo = track_features["tempo"]
        track_time_signature = track_features["time_signature"]
    except TypeError:
        # Handle the case where track_features is None
        track_danceability = None
        track_energy = None
        track_loudness = None
        track_speechiness = None
        track_acousticness = None
        track_instrumentalness = None
        track_liveness = None
        track_valence = None
        track_tempo = None
        track_time_signature = None

    # Add the track information to a list
    track_info.append((track_id, track_name, track_artist, track_popularity, track_duration,
                       track_album, track_release_date, track_danceability, track_energy, track_loudness,
                       track_speechiness, track_acousticness, track_instrumentalness, track_liveness, track_valence,
                       track_tempo, track_time_signature))

# Create a DataFrame with the track information
df = pd.DataFrame(track_info, columns=["id", "name", "artist", "popularity", "duration_ms",
                                       "album", "release_date", "danceability", "energy", "loudness",
                                       "speechiness", "acousticness", "instrumentalness", "liveness",
                                       "valence", "tempo", "time_signature"])

# Save the DataFrame to a CSV file
df.to_csv("calm_playlist.csv", index=False)
