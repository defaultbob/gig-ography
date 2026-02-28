"""
Setlist.fm API integration.

Two-path logic:
1. Search for an exact date match → return setlist URL, song count, top songs.
2. If no exact match → fetch artist's setlists from that year and compute averages.
"""

import os
import time
from collections import Counter

import requests

BASE_URL = "https://api.setlist.fm/rest/1.0"


def _headers() -> dict:
    return {
        "x-api-key": os.environ["SETLIST_FM_API_KEY"],
        "Accept": "application/json",
    }


def _get(path: str, params: dict | None = None) -> dict | None:
    """Make a GET request; return JSON dict or None on error."""
    try:
        resp = requests.get(f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
    except Exception as exc:
        print(f"    [setlist.fm] Error: {exc}")
    return None


def _iso_to_setlistfm(date_iso: str) -> str:
    """Convert YYYY-MM-DD to DD-MM-YYYY (setlist.fm format)."""
    parts = date_iso.split("-")
    return f"{parts[2]}-{parts[1]}-{parts[0]}"


def _count_songs(setlist: dict) -> int:
    return sum(len(s.get("song", [])) for s in setlist.get("sets", {}).get("set", []))


def _extract_songs(setlist: dict, n: int = 5) -> list[str]:
    songs = []
    for s in setlist.get("sets", {}).get("set", []):
        for song in s.get("song", []):
            name = song.get("name", "").strip()
            if name:
                songs.append(name)
    return songs[:n]


def get_setlist(artist: str, date: str) -> dict:
    """
    Return enrichment data for a specific artist + date.
    Falls back to tour average if no exact setlist is found.
    """
    setlist_date = _iso_to_setlistfm(date)
    year = date[:4]

    data = _get("/search/setlists", {"artistName": artist, "date": setlist_date, "p": 1})
    time.sleep(0.5)  # respect rate limits

    if data and data.get("setlist"):
        sl = data["setlist"][0]
        return {
            "setlist_url": sl.get("url"),
            "total_songs": _count_songs(sl),
            "top_songs": _extract_songs(sl),
        }

    print(f"    [setlist.fm] No exact match for {artist} on {date}. Calculating tour average.")
    return _calculate_average_setlist(artist, year)


def _calculate_average_setlist(artist: str, year: str) -> dict:
    """Fetch all setlists for an artist in a given year and compute averages."""
    all_songs: list[str] = []
    song_counts: list[int] = []
    page = 1

    while True:
        data = _get("/search/setlists", {"artistName": artist, "year": year, "p": page})
        time.sleep(0.5)
        if not data or not data.get("setlist"):
            break

        for sl in data["setlist"]:
            count = _count_songs(sl)
            if count > 0:
                song_counts.append(count)
                all_songs.extend(s.get("name", "") for set_ in sl.get("sets", {}).get("set", []) for s in set_.get("song", []))

        total_pages = (data.get("total", 0) + data.get("itemsPerPage", 20) - 1) // data.get("itemsPerPage", 20)
        if page >= total_pages or page >= 5:  # cap at 5 pages to avoid abuse
            break
        page += 1

    avg_songs = round(sum(song_counts) / len(song_counts)) if song_counts else None
    top_recurring = [song for song, _ in Counter(all_songs).most_common(5) if song.strip()]

    return {
        "setlist_url": None,
        "total_songs": avg_songs,
        "top_songs": top_recurring,
    }
