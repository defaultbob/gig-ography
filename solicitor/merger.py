"""
Merges email-parsed gigs with manual_entries.yaml.

Conflict rule: email data overrides manual entry's date/year.
All other empty fields are filled from whichever source has data.
"""

import yaml


def merge_sources(email_gigs: list[dict], manual_yaml_path: str) -> list[dict]:
    """
    Merge email-sourced gigs with manual entries.
    Returns a deduplicated list with email data winning on date conflicts.
    """
    try:
        with open(manual_yaml_path, encoding="utf-8") as f:
            manual_gigs = yaml.safe_load(f) or []
    except FileNotFoundError:
        manual_gigs = []

    # Build lookup: (normalised_artist, year) -> manual entry
    manual_map = {}
    for gig in manual_gigs:
        key = _make_key(gig)
        manual_map[key] = gig

    merged = []
    seen_keys = set()

    for email_gig in email_gigs:
        key = _make_key(email_gig)
        seen_keys.add(key)

        if key in manual_map:
            # Merge: email wins on date; fill other empty fields from manual
            manual_gig = manual_map[key]
            merged_gig = {**manual_gig, **email_gig}
            # Restore manual-only fields that email left empty
            for field, value in manual_gig.items():
                if not email_gig.get(field) and value:
                    merged_gig[field] = value
        else:
            merged_gig = email_gig

        merged.append(merged_gig)

    # Append manual-only entries (not found in email)
    for gig in manual_gigs:
        if _make_key(gig) not in seen_keys:
            merged.append(gig)

    return merged


def _make_key(gig: dict) -> tuple[str, str]:
    """Normalised (artist, year) tuple used as the deduplication key."""
    artist = (gig.get("artist") or "").lower().strip()
    year = str(gig.get("date") or "")[:4]
    return (artist, year)
