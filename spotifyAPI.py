import spotipy
import time
from IPython.display import clear_output
from spotipy import SpotifyClientCredentials, util, oauth2


client_id = "8af68ba9ec0e4d23aa6f3b3df73989e2"
client_secret = "a9b8aa3b0a5f499b84acbcd909b17c86"
redirect_uri = "http://localhost:5000/callback"
username = "mhfmtzz9e96snjn9ajhifx51k"
scope = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"

# Credentials to access the Spotify Music Data
manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager)

# Credentials to access to  the Spotify User's Playlist, Favorite Songs, etc. 
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri) 
spt = spotipy.Spotify(auth=token)

def authorize_user():
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

def get_token(code):
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        return token_info['access_token']
    else:
        return None

def set_token(token):
    sp = spotipy.Spotify(auth=token)

def get_user_playlists():
    playlists = sp.current_user_playlists()
    return playlists

def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks += results['items']
    while results['next']:
        results = sp.next(results)
        tracks += results['items']
    return tracks

def create_playlist(playlist_name, track_ids):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name)
    sp.playlist_add_items(playlist['id'], track_ids)
    return playlist

def get_songs_features(id):

    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    id =  meta['id']
    name = meta['name']
    artist = meta['album']['artists'][0]['name']
    popularity = meta['popularity']
    duration = meta['duration_ms']
    album = meta['album']['name']
    release_date = meta['album']['release_date']

    # features
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    acousticness = features[0]['acousticness']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [id, name, artist, popularity, duration, album, release_date, danceability, energy,
            loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature]
    columns = ['id','name','artist','popularity','duration','album','release_date','danceability','energy','loudness','speechiness',
                'acousticness','instrumentalness','liveness','valence','tempo','time_signature']
    
    return track, columns

