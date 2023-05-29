from flask import Flask, render_template, request, redirect, session
from spotifyAPI import *
from model import *

app = Flask(__name__)
app.secret_key = "N57ouRoGV4"

@app.route('/')
def index():
    login_url = authorize_user()
    return render_template('login.html', login_url=login_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = get_token(code)
    if token:
        set_token(token)
        session['token'] = token
        return redirect('/main')
    else:
        return "Failed to retrieve access token."

@app.route('/main')
def main():
    token = session.get('token')
    if not token:
        return redirect('/')
    set_token(token)
    playlists = get_user_playlists()
    moods = target['mood'].tolist()
    return render_template('main.html', playlists=playlists, moods=moods)

@app.route('/playlist', methods=['POST'])
def generate_playlist():
    playlist_id = request.form['playlist_id']
    mood = request.form['mood']
    tracks = get_playlist_tracks(playlist_id)
    filtered_tracks = []

    for track in tracks:
        track_id = track['track']['id']
        name, artist, predicted_mood = predict_mood(track_id)
        if predicted_mood == mood:
            filtered_tracks.append(track_id)

    if len(filtered_tracks) > 0:
        playlist_name = f"{mood} Playlist"
        created_playlist = create_playlist(playlist_name, filtered_tracks)
        return render_template('playlist.html', playlist_name=playlist_name, tracks=filtered_tracks)
    else:
        return "No songs matching the selected mood were found."

if __name__ == '__main__':
    app.run(debug=True)
