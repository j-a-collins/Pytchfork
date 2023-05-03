"""
Imports the data from the .csv and adds the new albums
to a Spotify playlist.

J A Collins 14-08-2022
"""

import pandas as pd
import spotipy
import re
from spotipy.oauth2 import SpotifyOAuth
from creds import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, PLAYLIST_ID


class SpotifyPlaylistAdder:
    def __init__(self, client_id, client_secret, redirect_uri, scope, playlist_id):
        self.sp = self.initialize_spotify(client_id, client_secret, redirect_uri, scope)
        self.playlist_id = playlist_id

    @staticmethod
    def initialize_spotify(client_id, client_secret, redirect_uri, scope):
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            redirect_uri=redirect_uri,
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    @staticmethod
    def format_artists(name):
        pattern = r"([a-z])([A-Z])"
        return re.sub(pattern, r"\1 \2", name)

    def search_album(self, artist, album_title):
        query = f"artist:{artist} album:{album_title}"
        results = self.sp.search(q=query, type="album", limit=1)

        if results["albums"]["items"]:
            return results["albums"]["items"][0]["id"]
        else:
            return None

    def add_album_to_playlist(self, album_id, artist, album_title):
        album_tracks = self.sp.album_tracks(album_id)
        track_ids = [track["id"] for track in album_tracks["items"]]
        self.sp.playlist_add_items(self.playlist_id, track_ids)

        print(
            f"Tracks from album '{album_title}' by '{artist}' added to the playlist with ID '{self.playlist_id}'"
        )

    def add_albums_from_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        df["artist"] = df["artist"].apply(self.format_artists)

        for _, row in df.iterrows():
            artist, album_title = row["artist"], row["title"]
            album_id = self.search_album(artist, album_title)

            if album_id:
                self.add_album_to_playlist(album_id, artist, album_title)
            else:
                print(f"Album '{album_title}' by '{artist}' not found")


def main():
    playlist_adder = SpotifyPlaylistAdder(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri="http://localhost:8080/callback",
        scope="playlist-modify-public",
        playlist_id=PLAYLIST_ID,
    )

    playlist_adder.add_albums_from_csv("best-new-albums.csv")


if __name__ == "__main__":
    main()
