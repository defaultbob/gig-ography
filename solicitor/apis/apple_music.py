"""
Apple Music artist URL lookup via apple-music-python.

Requires:
  APPLE_MUSIC_KEY_ID     — from Apple Developer console (MusicKit key)
  APPLE_MUSIC_TEAM_ID    — your Apple Developer Team ID
  APPLE_MUSIC_SECRET_KEY_PATH — local path to the .p8 private key file

Note: An Apple Developer Program membership ($99/yr) is required to generate
MusicKit keys. If credentials are not configured, this module returns None
gracefully so the rest of enrichment is unaffected.
"""

import os
from typing import Optional

import applemusicpy #


def get_artist_url(artist_name: str) -> Optional[str]:
    """Return the Apple Music artist URL, or None if unavailable."""
    key_id = os.environ.get("APPLE_MUSIC_KEY_ID")
    team_id = os.environ.get("APPLE_MUSIC_TEAM_ID")
    key_path = os.environ.get("APPLE_MUSIC_SECRET_KEY_PATH")

    if not all([key_id, team_id, key_path]):
        return None

    try:
        secret_key = open(key_path, encoding="utf-8").read()
        am = applemusicpy.AppleMusic(
            secret_key=secret_key,
            key_id=key_id,
            team_id=team_id,
        )
        results = am.search(artist_name, types=["artists"], limit=1) #
        artists = results.get("results", {}).get("artists", {}).get("data", [])
        if artists:
            return artists[0]["attributes"]["url"]
    except Exception as exc:
        print(f"    [apple_music] Error for {artist_name!r}: {exc}")
    return None
