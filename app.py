from flask import Flask, render_template, request, jsonify
import core
import pandas as pd
from spotipy_search import SpotifyPlaylistAdder
from creds import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, PLAYLIST_ID

app = Flask(__name__, static_folder="static")

playlist_adder = SpotifyPlaylistAdder(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri="http://localhost:8080/callback",
    scope="playlist-modify-public",
    playlist_id=PLAYLIST_ID,
)


@app.route("/", methods=["GET", "POST"])
def home():
    albums = None  # Initialize albums as None

    if request.method == "POST":
        # Run your core program
        core.main()
        # Read the CSV file
        albums_df = pd.read_csv("best-new-albums.csv")
        # Convert the dataframe to dictionary before passing to template
        albums = albums_df.to_dict("records")

    return render_template("home.html", albums=albums)


@app.route("/add_album", methods=["POST"])
def add_album():
    data = request.json
    artist = data["artist"]
    album_title = data["album"]
    album_id = playlist_adder.search_album(artist, album_title)

    if album_id:
        playlist_adder.add_album_to_playlist(album_id, artist, album_title)
        return (
            jsonify(
                {
                    "message": f"Album '{album_title}' by '{artist}' added to the playlist"
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"message": f"Album '{album_title}' by '{artist}' not found"}),
            404,
        )


if __name__ == "__main__":
    app.run(debug=True)
