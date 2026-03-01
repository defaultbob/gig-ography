"""
Spotify artist URL lookup via spotipy (Client Credentials flow — no user login needed).

Requires SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in the environment.
"""

import spotipy
from typing import Optional #
from spotipy.oauth2 import SpotifyClientCredentials


def get_artist_url(artist_name: str) -> Optional[str]:
    """Return the Spotify artist URL for the given artist name, or None."""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1) #
        items = results["artists"]["items"]
        if items:
            return items[0]["external_urls"]["spotify"]
    except Exception as exc:
        print(f"    [spotify] Error for {artist_name!r}: {exc}")
    return None
