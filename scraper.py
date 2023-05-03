"""
Scrapes the 'best new music' from
pitchfork and adds them to a .csv

J A Collins 14-08-2022
"""

# Imports
import bs4.element
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os.path


def main():
    file_exists = check_file()
    reviews_raw = request_text()
    albums_df = get_fields(reviews_raw)
    albums_df.to_csv("./best-new-albums.csv", index=False)


def compare_files():
    [line.strip() for line in open("./best-new-albums.csv")]


def check_file() -> bool:
    """Check if file already exists"""
    return os.path.isfile("best-new-albums.csv")


def request_text() -> bs4.element.ResultSet:
    """Fetches the raw text of the given URL
    converts for readability and finds the reviews"""
    request = requests.get("https://pitchfork.com/reviews/best/albums/?page=1")
    try:
        print(f"Status code: {request.status_code}")
        cleaned_text = BeautifulSoup(request.text, "lxml")
        reviews_set = cleaned_text.find_all("div", {"class": "review"})
        return reviews_set
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def get_fields(raw: bs4.element.ResultSet) -> pd.DataFrame:
    """Splits the raw reviews into the required fields:
    Artist, Album, Genre"""
    all_albums = []  # This will hold all the dictionaries
    for album in raw:
        entry = {
            # Artist: 'ul'
            "artist": album.find_all(["ul"])[0].text,
            # Album: 'h2'
            "title": album.find_all(["h2"])[0].text,
            # Genre: 'li: genre-list__item'
            "genre": [
                genre.text
                for genre in album.find_all("li", {"class": "genre-list__item"})
            ],
        }
        all_albums.append(entry)
    return pd.DataFrame(all_albums)


if __name__ == "__main__":
    main()
