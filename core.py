"""
A program to fetch well-reviewed new music
and add it to a Spotify playlist.
Remember: give it a chance, exercise your
brain's neuroplasticity!

J A Collins 14-08-2022
"""

import scraper
import spotipy_search


def main():
    scraper.main()
    spotipy_search.main()


if __name__ == "__main__":
    main()
