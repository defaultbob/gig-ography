"""
Enrichment orchestrator.

For each gig, calls the four enrichment APIs in order and fills
only empty/null fields — never overwrites data that's already present.
"""

from apis import setlist_fm, musicbrainz, spotify, apple_music


def enrich_gigs(gigs: list[dict]) -> list[dict]:
    """Return a new list of gigs with enrichment data filled in."""
    enriched = []
    total = len(gigs)
    for i, gig in enumerate(gigs, 1):
        artist = gig.get("artist", "")
        date = gig.get("date", "")
        print(f"  [{i}/{total}] Enriching: {artist} ({date})")
        enriched.append(_enrich_one(gig))
    return enriched


def _enrich_one(gig: dict) -> dict:
    gig = dict(gig)  # shallow copy
    artist = gig.get("artist", "")
    date = gig.get("date", "")

    # 1. Setlist data (skip if all fields already populated)
    if _needs("setlist_url", gig) or _needs("total_songs", gig) or _needs("top_songs", gig):
        if date:
            try:
                sl_data = setlist_fm.get_setlist(artist, date)
                if _needs("setlist_url", gig):
                    gig["setlist_url"] = sl_data.get("setlist_url")
                if _needs("total_songs", gig):
                    gig["total_songs"] = sl_data.get("total_songs")
                if _needs("top_songs", gig):
                    gig["top_songs"] = sl_data.get("top_songs") or []
            except Exception as exc:
                print(f"    [setlist.fm] Failed: {exc}")

    # 2. Artist image
    if _needs("image_url", gig):
        try:
            url = musicbrainz.get_artist_image(artist)
            gig["image_url"] = url
        except Exception as exc:
            print(f"    [musicbrainz] Failed: {exc}")

    # 3. Spotify
    streaming = gig.setdefault("streaming", {})
    if _needs("spotify", streaming):
        try:
            streaming["spotify"] = spotify.get_artist_url(artist)
        except Exception as exc:
            print(f"    [spotify] Failed: {exc}")

    # 4. Apple Music
    if _needs("apple", streaming):
        try:
            streaming["apple"] = apple_music.get_artist_url(artist)
        except Exception as exc:
            print(f"    [apple_music] Failed: {exc}")

    return gig


def _needs(field: str, obj: dict) -> bool:
    """Return True if the field is missing or null/empty."""
    val = obj.get(field)
    if val is None:
        return True
    if isinstance(val, (list, str)) and not val:
        return True
    return False
