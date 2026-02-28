"""
Artist image enrichment via MusicBrainz → Wikipedia → Wikimedia Commons.

This is the most reliable free approach for artist images:
1. Search MusicBrainz for the artist and get their ID.
2. Fetch URL relations to find the Wikipedia page link.
3. Call the Wikipedia REST API to get the thumbnail image URL.
"""

import os
import time

import musicbrainzngs
import requests


def _setup():
    email = os.environ.get("MUSICBRAINZ_APP_EMAIL", "unknown@example.com")
    musicbrainzngs.set_useragent("gig-ography", "1.0", email)


def get_artist_image(artist_name: str) -> str | None:
    """Return a direct image URL for the given artist, or None."""
    _setup()
    try:
        result = musicbrainzngs.search_artists(artist=artist_name, limit=1)
        time.sleep(1)  # MusicBrainz rate limit: 1 req/sec for unregistered apps
        artists = result.get("artist-list", [])
        if not artists:
            return None

        artist_id = artists[0]["id"]
        artist_data = musicbrainzngs.get_artist_by_id(artist_id, includes=["url-rels"])
        time.sleep(1)

        relations = artist_data["artist"].get("url-relation-list", [])
        for rel in relations:
            url = rel.get("url", {}).get("resource", "")
            if "wikipedia.org/wiki/" in url:
                page_title = url.split("/wiki/")[-1]
                return _fetch_wikipedia_thumbnail(page_title)

    except Exception as exc:
        print(f"    [musicbrainz] Error for {artist_name!r}: {exc}")
    return None


def _fetch_wikipedia_thumbnail(page_title: str) -> str | None:
    """Fetch the thumbnail image URL from the Wikipedia page summary API."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}"
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "gig-ography/1.0"})
        if resp.ok:
            return resp.json().get("thumbnail", {}).get("source")
    except Exception as exc:
        print(f"    [wikipedia] Error fetching thumbnail for {page_title!r}: {exc}")
    return None
